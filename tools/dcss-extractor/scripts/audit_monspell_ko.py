#!/usr/bin/env python3
"""Check DCSS 0.34.1 Korean monster-spell speeches against the source DB.

Localized entries may omit English pronoun/preposition grammatical tokens
when those meanings have been incorporated into a Korean sentence. Identity,
target, beam, god, and database-reference tokens are required.
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

SEPARATOR = re.compile(r"^%%%%[^\r\n]*$", re.M)
MARKER = re.compile(r"@([^@\n]+)@")
ALT = re.compile(r"\[[^\[\]\n]*\|[^\[\]\n]*\]")
OMITTABLE_GRAMMAR = {"at", "possessive", "reflexive", "arms", "subjective"}
WEIGHT = re.compile(r"^w:\d+$")
HANGUL = re.compile(r"[가-힣]")


def parse(text):
    parsed = {}
    duplicate = []
    for block in SEPARATOR.split(text)[1:]:
        lines = block.splitlines()
        ki = next((i for i, line in enumerate(lines)
                   if line.strip() and not line.lstrip().startswith("#")), None)
        if ki is None:
            continue
        key = lines[ki].strip()
        body = [line.strip() for line in lines[ki + 1:]
                if line.strip() and not line.lstrip().startswith("#")]
        if key in parsed:
            duplicate.append(key)
        else:
            parsed[key] = body
    return parsed, duplicate


def visible_lines(body):
    return [line for line in body if not WEIGHT.fullmatch(line)]


def structural_issues(english, korean):
    issues = []
    if not korean:
        issues.append("empty_body")
        return issues
    es, ks = visible_lines(english), visible_lines(korean)
    if len(es) != len(ks):
        issues.append("variant_count")
        return issues
    ew = [line for line in english if WEIGHT.fullmatch(line)]
    kw = [line for line in korean if WEIGHT.fullmatch(line)]
    if ew != kw:
        issues.append("weight_list")
    for i, (source, translation) in enumerate(zip(es, ks)):
        required = Counter(token for token in MARKER.findall(source)
                           if token not in OMITTABLE_GRAMMAR)
        actual = Counter(MARKER.findall(translation))
        if required != actual:
            issues.append(f"line_{i+1}_required_markers")
        if len(ALT.findall(source)) != len(ALT.findall(translation)):
            issues.append(f"line_{i+1}_alternatives")
        for prefix in ("SOUND:", "VISUAL:", "SILENT:"):
            if source.startswith(prefix) != translation.startswith(prefix):
                issues.append(f"line_{i+1}_{prefix}_prefix")
        if not HANGUL.search(translation) and not translation.startswith(
                ("__NONE", "@")):
            issues.append(f"line_{i+1}_no_korean")
    return issues


def audit(original, localized):
    en, en_duplicates = parse(original)
    ko, ko_duplicates = parse(localized)
    issues = []
    for key in ko:
        if key not in en:
            issues.append({"key": key, "issue": "unknown_source_key"})
            continue
        for issue in structural_issues(en[key], ko[key]):
            issues.append({"key": key, "issue": issue})
    for key in ko_duplicates:
        issues.append({"key": key, "issue": "duplicate_korean_key"})
    return {
        "original_unique_keys": len(en),
        "translated_unique_keys": len(ko),
        "matching_keys": len(set(en) & set(ko)),
        "untranslated_keys": len(set(en) - set(ko)),
        "original_duplicate_keys": en_duplicates,
        "issues": issues,
        "limitations": [
            "Matching keys and tokens are not an evaluation of translation style.",
            "Korean particles and translated dynamic names need runtime verification.",
            "The engine accepts five-percent delimiters by checking the first four percent signs.",
            "No localized entry is required for __NONE or untouched legacy text.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--localized", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.original.read_text(encoding="utf-8-sig"),
                   args.localized.read_text(encoding="utf-8-sig"))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    if result["issues"]:
        raise SystemExit(f"Monster spell translation structural issues: {len(result['issues'])}")


if __name__ == "__main__":
    main()
