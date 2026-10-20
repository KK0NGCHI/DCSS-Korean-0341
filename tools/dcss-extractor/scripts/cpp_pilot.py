"""CPP-PILOT-001: conservative, read-only C++ string literal inventory."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter_cpp

PILOT = ("message.cc", "invent.cc", "describe.cc", "newgame.cc")
STRING_TYPES = {"string_literal", "raw_string_literal"}
OUTPUT_HINTS = ("mpr", "mprf", "cprintf", "printf", "set_title", "draw_desc", "add_text", "add_item", "add_entry", "formatted_string", "describe", "prompt", "message", "text", "title")
FIELDS = ("id","file","line","column","start_byte","end_byte","node_type","literal","call_expression","classification","reason","source_sha256")

def nearest_call(node, data):
    parent = node.parent
    while parent is not None:
        if parent.type == "call_expression":
            fn = parent.child_by_field_name("function")
            return data[fn.start_byte:fn.end_byte].decode("utf-8", "replace") if fn else ""
        if parent.type in ("function_definition", "translation_unit"):
            break
        parent = parent.parent
    return ""

def classify(call):
    if not call:
        return "unknown", "no_enclosing_call"
    low = call.lower()
    if any(h in low for h in OUTPUT_HINTS):
        return "candidate_visible", "output_like_call_unverified"
    return "unknown", "call_requires_review"

def extract_file(path, parser):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    tree = parser.parse(data)
    root = tree.root_node
    stack = [root]
    rows = []
    errors = []
    while stack:
        node = stack.pop()
        if node.type == "ERROR" or node.is_missing:
            errors.append({"file": path.name, "line": node.start_point.row + 1,
                           "type": node.type, "start_byte": node.start_byte})
        if node.type in STRING_TYPES:
            raw = data[node.start_byte:node.end_byte].decode("utf-8", "replace")
            call = nearest_call(node, data)
            classification, reason = classify(call)
            rows.append({"id": hashlib.sha256((path.name+":"+str(node.start_byte)+":"+raw).encode("utf-8")).hexdigest()[:20],
                         "file": path.name, "line": node.start_point.row + 1,
                         "column": node.start_point.column + 1, "start_byte": node.start_byte,
                         "end_byte": node.end_byte, "node_type": node.type,
                         "literal": raw, "call_expression": call,
                         "classification": classification, "reason": reason,
                         "source_sha256": digest})
        stack.extend(reversed(node.children))
    return rows, errors, {"file":path.name,"sha256":digest,"bytes":len(data),
                          "literal_nodes":len(rows),"parse_errors":len(errors),
                          "root_has_error":root.has_error}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    parser = Parser(Language(tree_sitter_cpp.language()))
    args.output.mkdir(parents=True, exist_ok=True)
    all_rows, all_errors, files, failures = [], [], [], []
    for name in PILOT:
        path = args.source / name
        try:
            rows, errors, info = extract_file(path, parser)
            all_rows.extend(rows)
            all_errors.extend(errors)
            files.append(info)
            print(f"{name}: literals={len(rows)}, parse_errors={len(errors)}")
        except (OSError, ValueError) as exc:
            failures.append({"file":name,"error":str(exc)})
            print(f"{name}: FAILED: {exc}")
    with (args.output / "strings.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)
    (args.output / "strings.json").write_text(json.dumps(all_rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report = {"batch":"CPP-PILOT-001","generated_utc":datetime.now(timezone.utc).isoformat(),
              "source_root":str(args.source.resolve()),"files":files,"failures":failures,
              "parse_errors":all_errors,"total_literal_nodes":len(all_rows),
              "unique_literal_spellings":len({r["literal"] for r in all_rows}),
              "classification_counts":dict(Counter(r["classification"] for r in all_rows)),
              "limitations":["AST literal nodes only; preprocessor branches, macros and runtime-generated strings need later audit.",
                             "Call-based visibility is heuristic and not confirmed player-visible.",
                             "Parse errors do not automatically invalidate all extracted nodes.",
                             "No translation catalog is produced in this pilot."]}
    (args.output / "summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"TOTAL literals={len(all_rows)}, unique={report['unique_literal_spellings']}, errors={len(all_errors)}, failures={len(failures)}")
    print(f"Output: {args.output.resolve()}")
    if failures:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
