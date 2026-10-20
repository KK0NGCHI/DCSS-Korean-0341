"""Crash-safe audit of existing CPP-PILOT-001 outputs.

No Tree-sitter import or native parser calls. Reads existing summary.json and
strings.csv, reconstructs physical line/column from source byte offsets.
"""
import argparse
import bisect
import collections
import csv
import json
from pathlib import Path

FILES=("message.cc","invent.cc","describe.cc","newgame.cc")

def line_starts(data):
    starts=[0]
    i=0
    while i<len(data):
        if data[i]==13:
            i+=2 if i+1<len(data) and data[i+1]==10 else 1
            starts.append(i)
        elif data[i]==10:
            i+=1
            starts.append(i)
        else:
            i+=1
    return starts

def pos(starts,offset):
    if not isinstance(offset,int) or offset<0:
        raise ValueError(f"Invalid offset: {offset}")
    k=bisect.bisect_right(starts,offset)-1
    return k+1,offset-starts[k]+1

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--pilot",type=Path,required=True)
    a=p.parse_args()
    summary=json.loads((a.pilot/"summary.json").read_text(encoding="utf-8"))
    with (a.pilot/"strings.csv").open(encoding="utf-8-sig",newline="") as f:
        old=list(csv.DictReader(f))
    by_file=collections.defaultdict(list)
    for r in old:by_file[r["file"]].append(r)
    err_by_file=collections.defaultdict(list)
    for e in summary["parse_errors"]:err_by_file[e["file"]].append(e)
    files=[]; errors=[]; rows=[]; call_counts=collections.Counter()
    for name in FILES:
        print(f"Processing {name}...",flush=True)
        data=(a.source/name).read_bytes()
        starts=line_starts(data)
        for e in err_by_file[name]:
            off=int(e["start_byte"])
            line,col=pos(starts,off)
            context=[]
            for ix in range(max(0,line-3),min(len(starts),line+2)):
                b=starts[ix+1] if ix+1<len(starts) else len(data)
                context.append({"line":ix+1,"text":data[starts[ix]:b].decode("utf-8","replace").rstrip("\r\n")[:350]})
            errors.append({"file":name,"type":e["type"],"line":line,"column_byte":col,
                           "start_byte":off,"previous_reported_line":e["line"],"context":context})
        for r in by_file[name]:
            off=int(r["start_byte"])
            line,col=pos(starts,off)
            call=r["call_expression"]
            if call:call_counts[call]+=1
            rows.append({**r,"line":line,"column":col,"previous_reported_line":r["line"]})
        files.append({"file":name,"bytes":len(data),"physical_lines":len(starts),
                      "lf_count":data.count(b"\n"),"cr_count":data.count(b"\r"),
                      "error_nodes":len(err_by_file[name]),"literal_nodes":len(by_file[name])})
    report={"batch":"CPP-PILOT-001-AUDIT-V2-SAFE","files":files,"error_count":len(errors),
            "errors":errors,"literal_count":len(rows),"call_counts":call_counts.most_common(80),
            "unknown_without_call":sum(r["classification"]=="unknown" and not r["call_expression"] for r in rows),
            "notes":["Uses existing Tree-sitter extraction; does not reparse source.",
                     "Corrects line positions using source byte offsets.",
                     "Cannot recover lost literals or infer call chains without a new parser pass."]}
    out=a.pilot/"audit-v2.json"
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (a.pilot/"audit-v2-strings.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else list(old[0]))
        w.writeheader();w.writerows(rows)
    print("FILES:")
    for item in files:print(item)
    print("ERROR NODES:",len(errors),"LITERALS:",len(rows))
    print("UNKNOWN WITHOUT CALL:",report["unknown_without_call"])
    print("TOP CALLS:",call_counts.most_common(15))
    print("FIRST ERRORS:")
    for e in errors[:12]:
        print(e["file"],"line",e["line"],"byte",e["start_byte"])
        for c in e["context"]:print(" ",c["line"],c["text"][:180])
    print("Saved:",out)

if __name__=="__main__":
    main()
