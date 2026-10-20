"""Read-only audit of CPP-PILOT-001 parse errors and classification coverage."""
import argparse
import collections
import csv
import json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--pilot",type=Path,required=True)
    a=p.parse_args()
    summary=json.loads((a.pilot/"summary.json").read_text(encoding="utf-8"))
    out=[]
    for e in summary["parse_errors"]:
        file=a.source/e["file"]
        lines=file.read_text(encoding="utf-8",errors="replace").splitlines()
        n=e["line"]
        context=[f"{i+1}: {lines[i]}" for i in range(max(0,n-3),min(len(lines),n+2))]
        out.append({"file":e["file"],"line":n,"node_type":e["type"],"valid_line":1<=n<=len(lines),"context":context})
    with (a.pilot/"strings.csv").open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    calls=collections.Counter(r["call_expression"] for r in rows if r["classification"]=="unknown")
    report={"error_count":len(out),"errors":out,"unknown_top_calls":calls.most_common(60),
            "unknown_without_call":sum(r["classification"]=="unknown" and not r["call_expression"] for r in rows),
            "note":"Context is diagnostic only. A parser ERROR does not prove lost literals."}
    target=a.pilot/"diagnostics.json"
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Error nodes:",len(out))
    print("Unknown with no enclosing call:",report["unknown_without_call"])
    print("Unknown top calls:",calls.most_common(15))
    print("Diagnostic report:",target)
    for item in out[:8]:
        print("\n",item["file"],item["line"],item["node_type"],"valid_line=",item["valid_line"])
        print("\n".join(item["context"]))
if __name__=="__main__":
    main()
