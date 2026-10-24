#!/usr/bin/env python3
"""Deduplicate and triage lexical DCSS player-visible translation candidates.

This is a REVIEW QUEUE, not a list of confirmed untranslated strings.
Input is FULL-INVENTORY-001/strings.csv from full_inventory_v1.py.
Only source code records marked visible_candidate or review_dynamic are included.

Example:
  python tools/dcss-extractor/scripts/triage_visible_v1.py \
    --inventory tools/dcss-extractor/output/FULL-INVENTORY-001/strings.csv \
    --output tools/dcss-extractor/output/FULL-INVENTORY-001/triage
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

STATUS_ORDER = {"visible_candidate": 0, "review_dynamic": 1}
P0_FILES = {
    "ability.cc", "beam.cc", "describe.cc", "god-abil.cc",
    "invent.cc", "message.cc", "mon-util.cc", "newgame.cc",
    "player.cc", "player-equip.cc", "spl-summoning.cc",
}
P1_PREFIXES = ("dat/", "lua/", "dlua/", "clua/")
LANGUAGE_CHARS = re.compile(r"[A-Za-z]")
HANGUL = re.compile(r"[가-힣]")
WHITESPACE = re.compile(r"\s+")


def normalize(literal):
    # Do not decode escapes, substitute placeholders, or concatenate literals:
    # that would erase the original reference needed for contextual review.
    raw = literal.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        raw = raw[1:-1]
    return WHITESPACE.sub(" ", raw).strip()


def review_kind(text):
    if HANGUL.search(text):
        return "contains_hangul"
    if LANGUAGE_CHARS.search(text):
        return "review_english_or_identifier"
    return "not_natural_language"


def tier(path):
    name = Path(path).name
    if name in P0_FILES:
        return "P0"
    if path.startswith(P1_PREFIXES) or name.endswith((".lua", ".des")):
        return "P1"
    return "P2"


def load_queue(path):
    groups = {}
    status_counts = Counter()
    skipped = Counter()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            status = row.get("status", "")
            family = row.get("family", "")
            if status not in STATUS_ORDER:
                skipped["other_status"] += 1
                continue
            if family not in {"cc", "cpp", "c", "h", "hpp", "lua", "des"}:
                skipped["non_code"] += 1
                continue
            norm = normalize(row.get("literal", ""))
            if not norm:
                skipped["empty_literal"] += 1
                continue
            status_counts[status] += 1
            # Group identical raw text, keeping all sample locations. No
            # contextual equivalence or automatic translation is assumed.
            unit_id = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]
            group = groups.setdefault(norm, {
                "unit_id": unit_id, "literal": norm, "review_kind": review_kind(norm),
                "priority": "P2", "occurrences": 0, "visible_occurrences": 0,
                "dynamic_occurrences": 0, "paths": set(), "locations": [],
            })
            group["occurrences"] += 1
            group["paths"].add(row["path"])
            if status == "visible_candidate":
                group["visible_occurrences"] += 1
            else:
                group["dynamic_occurrences"] += 1
            candidate_tier = tier(row["path"])
            if candidate_tier < group["priority"]:
                group["priority"] = candidate_tier
            if len(group["locations"]) < 12:
                group["locations"].append({
                    "path": row["path"], "line": row["line"],
                    "column": row["column"], "status": status,
                })
    return groups, status_counts, skipped


def write_queue(groups, destination):
    fields = [
        "unit_id", "priority", "review_kind", "visible_occurrences",
        "dynamic_occurrences", "occurrences", "path_count", "first_location",
        "sample_paths", "literal",
    ]
    sorted_groups = sorted(groups.values(), key=lambda item: (
        item["priority"],
        item["review_kind"] != "review_english_or_identifier",
        item["visible_occurrences"] == 0,
        -item["occurrences"],
        item["literal"].casefold(),
    ))
    destination.mkdir(parents=True, exist_ok=True)
    all_file = destination / "review_queue.csv"
    p0_file = destination / "p0_english_review.csv"
    with all_file.open("w", encoding="utf-8-sig", newline="") as all_stream, \
         p0_file.open("w", encoding="utf-8-sig", newline="") as p0_stream:
        full_writer = csv.DictWriter(all_stream, fieldnames=fields)
        p0_writer = csv.DictWriter(p0_stream, fieldnames=fields)
        full_writer.writeheader()
        p0_writer.writeheader()
        for group in sorted_groups:
            paths = sorted(group["paths"])
            first = group["locations"][0]
            item = {key: group[key] for key in fields if key in group}
            item.update({
                "path_count": len(paths),
                "first_location": f"{first['path']}:{first['line']}",
                "sample_paths": "; ".join(paths[:10]),
            })
            full_writer.writerow(item)
            if group["priority"] == "P0" and group["review_kind"] == "review_english_or_identifier":
                p0_writer.writerow(item)
    return sorted_groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.inventory.is_file():
        parser.error(f"Inventory CSV does not exist: {args.inventory}")
    groups, status_counts, skipped = load_queue(args.inventory)
    ordered = write_queue(groups, args.output)
    by_kind = Counter(g["review_kind"] for g in ordered)
    by_tier = Counter(g["priority"] for g in ordered)
    p0 = sum(g["priority"] == "P0" and
             g["review_kind"] == "review_english_or_identifier" for g in ordered)
    summary = {
        "inventory": str(args.inventory),
        "lexical_input_counts": dict(status_counts),
        "skipped_records": dict(skipped),
        "unique_literal_groups": len(ordered),
        "unique_groups_by_kind": dict(by_kind),
        "unique_groups_by_priority": dict(by_tier),
        "p0_english_review_groups": p0,
        "limitations": [
            "This is a heuristic queue, not confirmed untranslated output.",
            "Identical literal grouping may combine different meanings/contexts.",
            "Lexical inventory misses raw C++ strings and may include comments.",
            "Presence of Hangul does not certify correct or complete translation.",
            "Individual fragments and printf/dynamic composition require callsite review.",
        ],
    }
    (args.output / "triage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
