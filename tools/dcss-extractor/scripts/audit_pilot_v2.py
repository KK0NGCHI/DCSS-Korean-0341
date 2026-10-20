"""CPP-PILOT-001 audit v2: correct source line mapping and richer diagnostics.

Read-only with respect to source and existing extraction outputs.
"""
import argparse
import bisect
import collections
import csv
import json
from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter_cpp

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

def pos(starts,byte):
    k=bisect.bisect_right(starts,byte)-1
    return k+1,byte-starts[k]+1

def nearest_calls(node,data):
    found=[]
    p=node.parent
    while p is not None:
        if p.type=="call_expression":
            fn=p.child_by_field_name("function")
            if fn:
                found.append(data[fn.start_byte:fn.end_byte].decode("utf-8","replace"))
        p=p.parent
    return found

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--pilot",type=Path,required=True)
    args=ap.parse_args()
    parser=Parser(Language(tree_sitter_cpp.language()))
    old=json.loads((args.pilot/"summary.json").read_text(encoding="utf-8"))
    with (args.pilot/"strings.csv").open(encoding="utf-8-sig",newline="") as f:
        old_rows=list(csv.DictReader(f))
    old_by_file=collections.defaultdict(list)
    for r in old_rows:old_by_file[r["file"]].append(r)
    errors=[]; enriched=[]; files=[]; call_counts=collections.Counter()
    for name in FILES:
        data=(args.source/name).read_bytes()
        starts=line_starts(data)
        tree=parser.parse(data)
        stack=[tree.root_node]
        file_errors=0; file_literals=0
        while stack:
            node=stack.pop()
            if node.type=="ERROR" or node.is_missing:
                line,col=pos(starts,node.start_byte)
                context=[]
                for ix in range(max(0,line-3),min(len(starts),line+2)):
                    a=starts[ix];b=starts[ix+1] if ix+1<len(starts) else len(data)
                    context.append({"line":ix+1,"text":data[a:b].decode("utf-8","replace").rstrip("\r\n")[:350]})
                errors.append({"file":name,"type":node.type,"line":line,"column_byte":col,
                               "start_byte":node.start_byte,"end_byte":node.end_byte,
                               "tree_sitter_row":node.start_point.row+1,
                               "context":context})
                file_errors+=1
            if node.type in ("string_literal","raw_string_literal"):
                file_literals+=1
                line,col=pos(starts,node.start_byte)
                calls=nearest_calls(node,data)
                raw=data[node.start_byte:node.end_byte].decode("utf-8","replace")
                old_class="unknown"
                call=calls[0] if calls else ""
                if call:call_counts[call]+=1
                enriched.append({"file":name,"line":line,"column_byte":col,"start_byte":node.start_byte,
                                 "literal":raw,"nearest_call":call,"call_chain":calls,
                                 "context_kind":node.parent.type if node.parent else None,
                                 "tree_sitter_row":node.start_point.row+1})
            stack.extend(reversed(node.children))
        files.append({"file":name,"bytes":len(data),"physical_lines":len(starts),
                      "cr_count":data.count(b"\r"),"lf_count":data.count(b"\n"),
                      "tree_sitter_end_row":tree.root_node.end_point.row+1,
                      "error_nodes":file_errors,"literal_nodes":file_literals,
                      "previous_literal_nodes":len(old_by_file[name])})
    result={"batch":"CPP-PILOT-001-AUDIT-V2","files":files,
            "errors":errors,"error_count":len(errors),
            "strings":enriched,"call_counts":call_counts.most_common(80),
            "notes":["Physical lines count CR, LF, and CRLF; Tree-sitter points may differ for CR-only sources.",
                     "Visibility cannot be proven from nearest_call alone.",
                     "Error nodes may overlap; count is not lost-string count."]}
    output=args.pilot/"audit-v2.json"
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (args.pilot/"audit-v2-strings.csv").open("w",encoding="utf-8-sig",newline="") as f:
        fields=["file","line","column_byte","start_byte","literal","nearest_call","context_kind","tree_sitter_row"]
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in enriched:w.writerow({k:r[k] for k in fields})
    print("FILES:")
    for f in files:print(f)
    print("ERROR NODES:",len(errors),"LITERALS:",len(enriched))
    print("TOP CALLS:",call_counts.most_common(20))
    print("FIRST ERRORS:")
    for e in errors[:12]:
        print(e["file"],"physical line",e["line"],"byte",e["start_byte"],
              "TS row",e["tree_sitter_row"])
        for c in e["context"]:print(" ",c["line"],c["text"][:180])
    print("Saved:",output)
    if len(enriched)!=len(old_rows):
        print("WARNING: literal count differs from original extraction:",len(old_rows))

if __name__=="__main__":main()
