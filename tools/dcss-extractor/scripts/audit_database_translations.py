#!/usr/bin/env python3
"""Audit localized DCSS dat/database files with conservative metrics.

Top-level English files can already contain Korean. File/key presence does not
prove translated player-visible output. Missing localized files are allowed;
the game falls back to its original database on missing keys.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ENTRY = re.compile(r"^%%%%\s*$", re.M)
HANGUL = re.compile(r"[가-힣]")
LATIN = re.compile(r"[A-Za-z]{3,}")


def parsed_entries(content):
    entries = []
    for block in ENTRY.split(content)[1:]:
        lines = block.splitlines()
        key_line = next((i for i, line in enumerate(lines)
                         if line.strip() and not line.lstrip().startswith("#")), None)
        if key_line is None:
            continue
        key = lines[key_line].strip()
        body = "\n".join(lines[key_line + 1:]).strip()
        entries.append((key, body))
    return entries


def language_lines(content):
    """Approximate natural-language line counts, not a translation rate."""
    rows = []
    for _, body in parsed_entries(content):
        rows.extend(row.strip() for row in body.splitlines()
                    if row.strip() and not row.lstrip().startswith("#")
                    and not re.fullmatch(r"w:\d+", row.strip()))
    return {
        "korean_lines": sum(bool(HANGUL.search(x)) for x in rows),
        "no_hangul_with_latin": sum(bool(LATIN.search(x)) and not HANGUL.search(x)
                                   for x in rows),
        "body_lines": len(rows),
    }


def inspect_database(root):
    folder = root / "dat" / "database"
    if not folder.is_dir():
        raise FileNotFoundError(f"Missing dat/database under {root}")
    korean = folder / "ko"
    files = []
    issues = []
    for orig in sorted(folder.glob("*.txt")):
        original = orig.read_text(encoding="utf-8-sig")
        en_items = parsed_entries(original)
        en_keys = {key for key, _ in en_items}
        ko_file = korean / orig.name
        ko_items = (parsed_entries(ko_file.read_text(encoding="utf-8-sig"))
                    if ko_file.is_file() else [])
        ko_keys = {key for key, _ in ko_items}
        en_duplicate = sum(n-1 for n in Counter(key for key, _ in en_items).values()
                           if n > 1)
        ko_duplicate = sum(n-1 for n in Counter(key for key, _ in ko_items).values()
                           if n > 1)
        empty = sum(not body for _, body in ko_items)
        stats = language_lines(original)
        files.append({
            "file": orig.name,
            "original_unique_keys": len(en_keys),
            "original_duplicate_keys": en_duplicate,
            "localized_file_present": bool(ko_items) or ko_file.is_file(),
            "localized_unique_keys": len(ko_keys),
            "matched_keys": len(en_keys & ko_keys),
            "missing_localized_keys": len(en_keys - ko_keys),
            "extra_localized_keys": len(ko_keys - en_keys),
            "localized_duplicate_keys": ko_duplicate,
            "localized_empty_bodies": empty,
            **stats,
        })
        for key in sorted(ko_keys - en_keys):
            issues.append({"file": orig.name, "kind": "extra_localized_key", "key": key})
        for key, body in ko_items:
            if not body:
                issues.append({"file": orig.name, "kind": "empty_localized_body", "key": key})
        if ko_duplicate:
            issues.append({"file": orig.name, "kind": "duplicate_localized_key",
                           "key": f"{ko_duplicate} duplicate occurrences"})
    report = {
        "original_files": len(files),
        "localized_files": sum(f["localized_file_present"] for f in files),
        "original_unique_keys_sum": sum(f["original_unique_keys"] for f in files),
        "localized_matched_keys_sum": sum(f["matched_keys"] for f in files),
        "korean_lines_in_top_level_originals": sum(f["korean_lines"] for f in files),
        "latin_only_lines_in_top_level_originals": sum(
            f["no_hangul_with_latin"] for f in files),
        "files": files,
        "issues": issues,
        "limitations": [
            "Some top-level database content is already Korean, regardless of ko/ coverage.",
            "Header keys, macros and Lua-like tags may appear in Latin-only lines.",
            "Matched localized keys do not imply translation quality or runtime visibility.",
            "Missing translated files are not build errors; fallbacks remain in use.",
        ],
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = inspect_database(args.source)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    keys = report["files"][0].keys() if report["files"] else []
    with (args.output / "files.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        writer.writerows(report["files"])
    with (args.output / "issues.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["file", "kind", "key"])
        writer.writeheader()
        writer.writerows(report["issues"])
    compact = {k: v for k, v in report.items() if k not in {"files", "issues"}}
    compact["priority_files"] = [
        row for row in report["files"]
        if row["file"] in {"monspeak.txt", "monspell.txt", "godspeak.txt",
                          "wpnnoise.txt", "godname.txt", "shout.txt"}
    ]
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    # Fail only on structural problems in existing Korean overlays, not missing
    # translations. Extra localized keys may be intentional legacy assets.
    bad = [e for e in report["issues"]
           if e["kind"] in {"empty_localized_body", "duplicate_localized_key"}]
    if bad:
        raise SystemExit(f"Localized database structural problems: {len(bad)}")


if __name__ == "__main__":
    main()
