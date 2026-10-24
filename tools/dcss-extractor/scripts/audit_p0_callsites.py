#!/usr/bin/env python3
"""Inventory direct P0 C++ output *callsites*, independent of lexical-window guesses.

This static scanner is conservative: it masks C++ comments, string and
character literals to detect real function calls; it never declares a string
definitely untranslated or actually exercised at runtime.

Usage:
  python tools/dcss-extractor/scripts/audit_p0_callsites.py \
    --source source --output tools/dcss-extractor/output/P0-CALLSITE-001
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

P0_FILES = (
    "ability.cc", "beam.cc", "describe.cc", "god-abil.cc", "invent.cc",
    "message.cc", "mon-util.cc", "newgame.cc", "player.cc",
    "player-equip.cc", "spl-summoning.cc",
)
OUTPUT_NAMES = (
    "mpr", "mprf", "simple_god_message", "simple_monster_message",
    "yesno", "yesnoquit", "cprintf",
)
CALL = re.compile(r"\b(" + "|".join(OUTPUT_NAMES) + r")\s*\(")
STRING = re.compile(r'"(?:\\.|[^"\\])*"', re.S)
HANGUL = re.compile(r"[가-힣]")
ENGLISH = re.compile(r"[A-Za-z]{3,}")
PRINTF = re.compile(r"%(?:\d+\$)?[-+# 0]*(?:\d+|\*)?"
                    r"(?:\.(?:\d+|\*))?(?:hh|ll|[hljztL])?[diuoxXfFeEgGaAcspn%]")
TECHNICAL = re.compile(r"(?:<[^<>]*>|\$cmd\[[^\]]+\]|\\[nrt]|%[sd])")


def masked_code(src):
    """Return equal-length text with comments/literals replaced by spaces.

    Preserve newlines for stable line addresses. Handle standard C++ quoted
    literals and comments; raw C++ literals are treated conservatively as
    ordinary string delimiters and therefore require manual review.
    """
    out = list(src)
    n, i = len(src), 0

    def blank(a, b):
        for j in range(a, b):
            if src[j] not in "\r\n":
                out[j] = " "

    while i < n:
        if src.startswith("//", i):
            j = src.find("\n", i + 2)
            j = n if j < 0 else j
            blank(i, j)
            i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            blank(i, j)
            i = j
        elif src[i] in ("'", '"'):
            quote, j = src[i], i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                elif src[j] == quote:
                    j += 1
                    break
                else:
                    j += 1
            blank(i, min(j, n))
            i = j
        else:
            i += 1
    return "".join(out)


def end_of_call(masked, start):
    depth = 0
    for i in range(start, len(masked)):
        ch = masked[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    return None


def classify(msg, call):
    if not msg:
        return "no_direct_literal"
    if HANGUL.search(msg):
        return "contains_hangul"
    text = TECHNICAL.sub("", msg)
    text = PRINTF.sub("", text)
    if ENGLISH.search(text):
        if "MSGCH_DIAGNOSTICS" in call or "MSGCH_ERROR" in call:
            return "developer_or_error_review"
        return "english_output_review"
    return "format_or_symbol_only"


def scan_file(path, relative):
    source = path.read_text(encoding="utf-8-sig")
    mask = masked_code(source)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows = []
    for match in CALL.finditer(mask):
        open_at = mask.find("(", match.start(), match.end() + 1)
        if open_at < 0:
            continue
        end = end_of_call(mask, open_at)
        if end is None:
            continue
        call = source[match.start():end + 1]
        # Restrict review to textual literals on output-function callsites.
        literals = STRING.findall(call)
        if not literals:
            continue
        message = " ".join(s[1:-1] for s in literals[:3])
        line = source.count("\n", 0, match.start()) + 1
        classification = classify(message, call)
        rows.append({
            "id": f"{relative}:{line}:{match.group(1)}",
            "path": relative, "line": line, "function": match.group(1),
            "classification": classification,
            "first_literal": literals[0][1:-1],
            "literal_count": len(literals),
            "format_specifiers": sum(len(PRINTF.findall(s)) for s in literals),
            "call_excerpt": " ".join(call.split())[:400],
            "source_sha256": digest,
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error("Source directory missing")
    args.output.mkdir(parents=True, exist_ok=True)
    columns = [
        "id", "path", "line", "function", "classification", "first_literal",
        "literal_count", "format_specifiers", "call_excerpt", "source_sha256",
    ]
    counts = Counter()
    all_rows = []
    for file in P0_FILES:
        path = args.source / file
        if not path.exists():
            parser.error(f"Missing P0 source: {path}")
        found = scan_file(path, file)
        all_rows.extend(found)
        counts.update(row["classification"] for row in found)
    for name, rows in [
        ("all_callsites.csv", all_rows),
        ("english_callsites.csv", [r for r in all_rows
                                   if r["classification"] == "english_output_review"]),
    ]:
        with (args.output / name).open("w", newline="", encoding="utf-8-sig") as out:
            writer = csv.DictWriter(out, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
    report = {
        "files_scanned": len(P0_FILES),
        "direct_calls_with_literals": len(all_rows),
        "classifications": dict(sorted(counts.items())),
        "important_limits": [
            "The scanned functions are possible user-facing output, not proof of runtime reachability.",
            "The scanner may miss macro wrappers, indirect outputs, raw C++ strings and Lua.",
            "Nested functions may contain incidental literals; inspect call excerpts.",
            "English/identifier class does not equal untranslated natural-language text.",
            "Calls with no direct literal are omitted and may still produce English.",
        ],
    }
    (args.output / "summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("FIRST 50 ENGLISH OUTPUT CALLSITES:")
    print(json.dumps([{
        "id": row["id"], "literal": row["first_literal"],
        "call": row["call_excerpt"][:180],
    } for row in all_rows if row["classification"] == "english_output_review"][:50],
        ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
