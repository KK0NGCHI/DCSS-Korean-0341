"""Conservative inventory of simple C++ literals passed to output calls.

Produces a review-only POT and CSVs; does not claim runtime visibility.
Run on a core_review.csv from WHOLE-TRIAGE-001.
"""
import argparse
import ast
import collections
import csv
import json
import re
from pathlib import Path

SINKS = {"mpr", "mprf", "cprintf", "yesno", "yesnoquit",
         "prompt_for_quantity", "prompt_for_int"}
FORMAT = re.compile(r"%(?:\d+\$)?[-+ #0]*(?:\d+|\*)?(?:\.(?:\d+|\*))?(?:hh|ll|[hljztL])?[diuoxXfFeEgGaAcspn%]")

def decode_literal(value):
    if not (value.startswith('"') and value.endswith('"')):
        return None
    try:
        result = ast.literal_eval(value)
        return result if isinstance(result, str) else None
    except (ValueError, SyntaxError, UnicodeError):
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    candidates, review = [], []
    pot = collections.defaultdict(list)
    with args.input.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            literal = decode_literal(row["literal"])
            is_candidate = (
                row["triage_bucket"] == "direct_sink_candidate"
                and row["call_expression"].strip() in SINKS
                and literal is not None
                and bool(literal.strip())
                and len(literal) <= 1000
            )
            if is_candidate:
                status = "po_draft_review"
                if "%" in literal and not FORMAT.search(literal):
                    status = "format_or_percent_manual_review"
                if row["parse_error_overlap"].lower() == "true":
                    status = "parser_error_review"
                enriched = {**row, "decoded_text": literal,
                            "catalog_status": status, "translation": ""}
                candidates.append(enriched)
                if status == "po_draft_review":
                    pot[literal].append(enriched)
                else:
                    review.append(enriched)
            else:
                review.append({**row, "decoded_text": literal or "",
                               "catalog_status": "unresolved_review",
                               "translation": ""})
    columns = ["id", "file", "language", "line", "column", "literal",
               "decoded_text", "call_expression", "triage_bucket",
               "catalog_status", "translation", "source_sha256",
               "start_byte", "end_byte"]
    for filename, rows in (("output_candidates.csv", candidates),
                           ("manual_review.csv", review)):
        with (args.output / filename).open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    with (args.output / "draft.pot").open("w", encoding="utf-8") as f:
        f.write('msgid ""\nmsgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"\n\n')
        for message, rows in sorted(pot.items()):
            for row in rows[:30]:
                f.write(f'#: {row["file"]}:{row["line"]}\n')
            f.write("#. OUTPUT CANDIDATE ONLY; manually verify translation unit.\n")
            f.write("msgid " + json.dumps(message, ensure_ascii=False) + '\nmsgstr ""\n\n')
    summary = {"input_rows": len(candidates) + len(review),
               "candidate_occurrences": len(candidates),
               "pot_unique_msgids": len(pot),
               "pot_occurrences": sum(map(len, pot.values())),
               "manual_review_rows": len(review),
               "translation_confirmed": 0, "translated": 0}
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
