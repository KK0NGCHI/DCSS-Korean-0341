#!/usr/bin/env python3
"""Conservative review of the Korean monspeak.txt overlay.

Preserve monster/target identity, directive prefixes, weighted variants,
alternative choices and Lua fences. Grammar-only English target prepositions
and possessives can be integrated into the Korean sentence.
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

from audit_monspell_ko import parse, visible_lines, MARKER, ALT, WEIGHT, HANGUL

OMITTABLE = {"possessive", "at_foe", "to_foe", "surface", "reflexive"}
PREFIXES = ("VISUAL:", "SOUND:", "SILENT:")


LUA_CONTROL = re.compile(r"^(?:if|elseif|else|end)\b")
LUA_REFERENCE_RETURN = re.compile(r"""^return\s+(['"])(@[^@\n]+@)\1$""")
LUA_DYNAMIC_RETURN = re.compile(r"^return\s+you\.[a-zA-Z_]\w*\(")


def lua_non_display_line(source_line, localized_line, in_lua):
    """Permit unchanged Lua syntax, not untranslated string literals."""
    if not in_lua:
        return False
    en, ko = source_line.strip(), localized_line.strip()
    if en.startswith(("{{", "}}")) or LUA_CONTROL.match(en):
        return en == ko
    if LUA_REFERENCE_RETURN.fullmatch(en) or LUA_DYNAMIC_RETURN.match(en):
        return en == ko
    return False


def lua_control_changed(source_line, localized_line, in_lua):
    if not in_lua:
        return False
    en, ko = source_line.strip(), localized_line.strip()
    if en.startswith(("{{", "}}")) or LUA_CONTROL.match(en):
        return en != ko
    return False


def check_variants(source, korean):
    issues = []
    if not korean:
        return ["empty_body"]
    src, dst = visible_lines(source), visible_lines(korean)
    if len(src) != len(dst):
        return ["variant_count"]
    ew = [line for line in source if WEIGHT.fullmatch(line)]
    kw = [line for line in korean if WEIGHT.fullmatch(line)]
    if ew != kw:
        issues.append("weight_list")
    in_lua = False
    for i, (en, ko) in enumerate(zip(src, dst), 1):
        lua_here = in_lua or "{{" in en
        required = Counter(tag for tag in MARKER.findall(en)
                           if tag not in OMITTABLE)
        actual = Counter(tag for tag in MARKER.findall(ko)
                         if tag not in OMITTABLE)
        if required != actual:
            issues.append(f"line_{i}_markers")
        if len(ALT.findall(en)) != len(ALT.findall(ko)):
            issues.append(f"line_{i}_random_alternatives")
        if any(en.startswith(prefix) != ko.startswith(prefix)
               for prefix in PREFIXES):
            issues.append(f"line_{i}_directive_prefix")
        if en.count("{{") != ko.count("{{") or en.count("}}") != ko.count("}}"):
            issues.append(f"line_{i}_lua_fence")
        if lua_control_changed(en, ko, lua_here):
            issues.append(f"line_{i}_lua_control_modified")
        if not HANGUL.search(ko) and ko not in {"__NONE", "__NEXT"} \
                and not ko.startswith("@") \
                and not lua_non_display_line(en, ko, lua_here):
            issues.append(f"line_{i}_no_hangul")
        if "}}" in en:
            in_lua = False
        elif "{{" in en:
            in_lua = True
    return issues


def audit(original, translation):
    en, en_dupes = parse(original)
    ko, ko_dupes = parse(translation)
    problems = []
    for key, body in ko.items():
        if key not in en:
            problems.append({"key": key, "reason": "not_in_source"})
        else:
            for reason in check_variants(en[key], body):
                problems.append({"key": key, "reason": reason})
    for key in ko_dupes:
        problems.append({"key": key, "reason": "duplicate_korean_key"})
    return {
        "source_unique_keys": len(en),
        "source_duplicate_key_occurrences": len(en_dupes),
        "localized_keys": len(ko),
        "matched_keys": len(set(en) & set(ko)),
        "remaining_source_keys": len(set(en) - set(ko)),
        "problems": problems,
        "limitations": [
            "Source may contain embedded Lua and key references not covered by this static audit.",
            "Structural correctness is not natural-language quality or runtime proof.",
            "Missing localizations intentionally fall back to original speeches.",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--original", type=Path, required=True)
    p.add_argument("--localized", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = audit(args.original.read_text(encoding="utf-8-sig"),
                   args.localized.read_text(encoding="utf-8-sig"))
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    if result["problems"]:
        raise SystemExit(f"Monspeak overlay structure errors: {len(result['problems'])}")


if __name__ == "__main__":
    main()
