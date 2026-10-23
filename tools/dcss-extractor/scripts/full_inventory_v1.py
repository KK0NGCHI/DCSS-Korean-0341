"""Repository-wide conservative translation inventory (not a semantic parser).

Usage:
 python tools/dcss-extractor/scripts/full_inventory_v1.py --source source --output output/FULL-INVENTORY-001

The source tree is read-only. Every candidate retains path, line, literal,
context and status. Heuristic results must NOT be counted as confirmed visible.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

EXT = {".cc", ".cpp", ".c", ".h", ".hpp", ".lua", ".des"}
EXCLUDE_PARTS = {"contrib", "android-project", "rltiles", "build", ".git",
                 "node_modules", "__pycache__", "obj", "deps"}
STRINGS = re.compile(r'(?:"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27)', re.S)
SINKS = re.compile(r'\b(?:mprf?|cprintf|yesnoquit|yesno|crawl\.mpr|crawl\.tutorial_msg|print|text|add_child|set_text)\s*\(')
FMT = re.compile(r'%(?:\d+\$)?[-+ #0]*(?:\d+|\*)?(?:\.(?:\d+|\*))?(?:hh|ll|[hljztL])?[diuoxXfFeEgGaAcspn%]')

def entries(text):
    for block in re.split(r'^%%%%\s*$', text, flags=re.M)[1:]:
        lines = block.splitlines()
        first = next((i for i, x in enumerate(lines)
                      if x.strip() and not x.lstrip().startswith("#")), None)
        if first is None:
            continue
        key = lines[first].strip()
        yield key, "\n".join(lines[first + 1:]).strip(), first + 1

def chunks(source):
    for file in sorted(source.rglob("*")):
        if not file.is_file() or file.is_symlink():
            continue
        rel = file.relative_to(source).as_posix()
        if any(p in EXCLUDE_PARTS for p in file.relative_to(source).parts):
            continue
        if file.suffix.lower() in EXT or rel.startswith("dat/descript/"):
            yield file, rel

def emit(writer, counts, **data):
    writer.writerow(data)
    counts[data["status"]] += 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not (args.source / "Makefile").exists():
        ap.error("--source must be the DCSS source directory containing Makefile")
    args.output.mkdir(parents=True, exist_ok=True)
    cols = ["id", "path", "line", "column", "family", "key", "literal", "status",
            "reason", "source_sha256"]
    counts, errors, files, units = Counter(), [], 0, 0
    english, korean = {}, {}
    for lang, store in (("", english), ("ko/", korean)):
        folder = args.source / "dat/descript" / lang
        if folder.exists():
            for file in sorted(folder.glob("*.txt")):
                try:
                    store[file.name] = dict((key, body) for key, body, _ in
                                            entries(file.read_text(encoding="utf-8-sig")))
                except (OSError, UnicodeError) as exc:
                    errors.append({"path": str(file), "error": str(exc)})
    output = args.output / "strings.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, cols)
        writer.writeheader()
        for file, rel in chunks(args.source):
            files += 1
            try:
                raw = file.read_bytes()
                text = raw.decode("utf-8-sig")
            except (OSError, UnicodeError) as exc:
                errors.append({"path": rel, "error": str(exc)})
                continue
            digest = hashlib.sha256(raw).hexdigest()
            is_desc = rel.startswith("dat/descript/") and file.suffix == ".txt"
            # Only top-level English/Korean files use the description-key format.
            # Other nested files must not inflate coverage statistics.
            if is_desc and file.parent not in {args.source / "dat/descript", args.source / "dat/descript/ko"}:
                continue
            if is_desc:
                # English key coverage and translation body are separate properties.
                is_ko = rel.startswith("dat/descript/ko/")
                if is_ko:
                    continue
                base = file.name
                target = korean.get(base, {})
                for key, body, _ in entries(text):
                    units += 1
                    if key not in target:
                        status, reason = "translation_missing_key", "no_ko_key"
                    elif not target[key].strip():
                        status, reason = "translation_empty", "empty_ko_body"
                    elif (not re.search(r"[가-힣]", target[key])
                          and not re.fullmatch(r"\s*(?:\[\[[^]]+\]\]|<[^>]+>)\s*", target[key])
                          and len(target[key]) > 15):
                        status, reason = "review_english_body", "ko_entry_no_hangul"
                    else:
                        status, reason = "review_translation_present", "key_present_not_quality_verified"
                    line = text.find(key)
                    emit(writer, counts, id=f"{rel}:{key}", path=rel,
                         line=text.count("\n", 0, max(0, line)) + 1, column=1,
                         family="description", key=key, literal=body[:4000],
                         status=status, reason=reason, source_sha256=digest)
                continue
            if file.suffix.lower() not in EXT:
                continue
            # This scanner is intentionally lexical: comments/char literals may
            # be false positives, and raw C++ strings may be missed.
            for match in STRINGS.finditer(text):
                literal = match.group()
                if len(literal) < 5 or not re.search(r"[A-Za-z]{3}", literal):
                    continue
                line = text.count("\n", 0, match.start()) + 1
                start = text.rfind("\n", 0, match.start()) + 1
                prefix = text[start:match.start()]
                if re.match(r"\s*#\s*include\s*$", prefix):
                    status, reason = "internal_candidate", "include_path"
                elif prefix.lstrip().startswith(("//", "--", "# ")):
                    status, reason = "comment_candidate", "line_comment"
                elif "[KO TEST]" in literal:
                    status, reason = "test_marker", "smoke_test"
                elif SINKS.search(text[max(0, match.start()-120):match.start()]):
                    status, reason = "visible_candidate", "near_output_call"
                elif FMT.search(literal):
                    status, reason = "review_dynamic", "format_placeholder"
                else:
                    status, reason = "review_unknown", "lexical_literal"
                emit(writer, counts, id=f"{rel}:{line}:{match.start()-start+1}",
                     path=rel, line=line, column=match.start()-start+1,
                     family=file.suffix.lower().lstrip("."), key="",
                     literal=literal[:4000], status=status, reason=reason,
                     source_sha256=digest)
                units += 1
    summary = {
        "batch": "FULL-INVENTORY-001", "source": str(args.source),
        "files_scanned": files, "rows": units, "status_counts": dict(counts),
        "read_errors": errors, "english_description_files": sorted(english),
        "korean_description_files": sorted(korean),
        "limitations": [
            "C++/Lua/DES lexical scanner, not a parser or complete string census.",
            "Quoted strings in comments may be false positives; raw C++ strings may be missed.",
            "Descriptions are key-matched; non-Hangul text is a REVIEW candidate, not automatic untranslated.",
            "No runtime visibility, translation quality or build assertions.",
        ],
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("files_scanned", "rows", "status_counts", "read_errors")}, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
