"""CPP-PILOT-002: source-preserving C++ literal audit and AST context.
Run with the same --source as pilot 001. No source files are modified.
"""
import argparse
import bisect
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter_cpp

FILES = ("message.cc", "invent.cc", "describe.cc", "newgame.cc")
FIELDS = ("id","file","line","column","start_byte","end_byte","literal","call_expression","context_kind","classification","reason","preprocessor","parse_error_overlap","source_sha256")
VISIBLE = ("mpr","mprf","cprintf","set_title","add_text","add_item","add_entry","show_help","yesno","make_shared<ui::Text>","prompt")
INTERNAL = ("json_write","json_open","set_sync_id","get_string","sscanf","fprintf")
TOKEN = re.compile(rb'(?P<raw>(?:u8|u|U|L)?R"(?P<delimiter>[^()\\\s]{0,16})\((?P<rawbody>.*?)\)(?P=delimiter)")|(?P<quoted>(?:u8|u|U|L)?"(?:\\.|[^"\\])*")',re.S)
DIRECTIVE = re.compile(rb'^\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b(.*)$')
def starts(data):
    return [0]+[i+1 for i,c in enumerate(data) if c==10]
def loc(s,offset):
    n=bisect.bisect_right(s,offset)-1
    return n+1,offset-s[n]+1
def mask_noncode(data):
    """Mask comments and character literals, preserving offsets and newlines.
    Strings are preserved so the lexer can find them. Handles raw strings.
    """
    out=bytearray(data); i=0; n=len(data)
    while i<n:
        if data.startswith(b'//',i):
            j=data.find(b'\n',i); j=n if j<0 else j
            for k in range(i,j): out[k]=32
            i=j; continue
        if data.startswith(b'/*',i):
            j=data.find(b'*/',i+2); j=n if j<0 else j+2
            for k in range(i,j):
                if out[k] not in (10,13):out[k]=32
            i=j; continue
        m=TOKEN.match(data,i)
        if m:
            i=m.end();continue
        if data[i]==39:
            j=i+1
            while j<n:
                if data[j]==92:j+=2;continue
                if data[j]==39:j+=1;break
                if data[j]==10:break
                j+=1
            for k in range(i,min(j,n)):
                if out[k] not in (10,13):out[k]=32
            i=j;continue
        i+=1
    return bytes(out)
def directives(data):
    result=[]; active=[]
    offset=0
    for line in data.splitlines(keepends=True):
        m=DIRECTIVE.match(line)
        if m:
            kind=m.group(1).decode(); expr=m.group(2).decode('utf-8','replace').strip()
            result.append((offset,offset+len(line),kind,expr))
        offset+=len(line)
    return result
def enclosing(node, start, end):
    while node:
        if node.start_byte<=start and node.end_byte>=end:
            for child in node.children:
                if child.start_byte<=start and child.end_byte>=end:
                    found=enclosing(child,start,end)
                    if found:return found
            return node
        return None
def context(node,data):
    cur=node
    while cur:
        if cur.type=='call_expression':
            fn=cur.child_by_field_name('function')
            return ('call',data[fn.start_byte:fn.end_byte].decode('utf-8','replace') if fn else '')
        if cur.type in ('init_declarator','assignment_expression','field_initializer'):
            return ('assignment',data[cur.start_byte:min(cur.start_byte+120,cur.end_byte)].decode('utf-8','replace'))
        cur=cur.parent
    return ('none','')
def classify(kind,ctx):
    low=ctx.lower()
    if kind=='call' and any(x.lower() in low for x in VISIBLE):
        return 'candidate_visible','output_call_heuristic'
    if kind=='call' and any(x.lower() in low for x in INTERNAL):
        return 'internal_candidate','internal_call_heuristic'
    return 'unknown','manual_review'
def run_file(path,parser):
    data=path.read_bytes(); digest=hashlib.sha256(data).hexdigest(); s=starts(data)
    clean=mask_noncode(data); ds=directives(clean)
    tree=parser.parse(data); root=tree.root_node
    errors=[]; stack=[root]
    while stack:
        node=stack.pop()
        if node.type=='ERROR' or node.is_missing:
            line,col=loc(s,node.start_byte)
            errors.append(dict(file=path.name,line=line,column=col,start_byte=node.start_byte,end_byte=node.end_byte,type=node.type))
        stack.extend(reversed(node.children))
    rows=[]; spans=set()
    for m in TOKEN.finditer(clean):
        a,b=m.span()
        if any(x<=a<y for x,y,_,_ in ds):continue
        spans.add((a,b))
        node=enclosing(root,a,b)
        kind,ctx=context(node,data) if node else ('none','')
        classification,reason=classify(kind,ctx)
        line,col=loc(s,a)
        pre=[f'{k} {e}' for x,y,k,e in ds if x<a][-8:]
        rows.append(dict(id=hashlib.sha256((path.name+':'+str(a)+':'+str(b)).encode()).hexdigest()[:20],
            file=path.name,line=line,column=col,start_byte=a,end_byte=b,
            literal=data[a:b].decode('utf-8','replace'),call_expression=ctx if kind=='call' else '',
            context_kind=kind,classification=classification,reason=reason,
            preprocessor=' | '.join(pre),parse_error_overlap=any(x['start_byte']<=a<x['end_byte'] for x in errors),
            source_sha256=digest))
    return rows,errors,dict(file=path.name,bytes=len(data),sha256=digest,literals=len(rows),parse_errors=len(errors))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--baseline',type=Path)
    args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    parser=Parser(Language(tree_sitter_cpp.language()))
    all_rows=[];errors=[];files=[]
    for name in FILES:
        rows,err,info=run_file(args.source/name,parser)
        all_rows+=rows;errors+=err;files.append(info)
        print(f'{name}: literals={len(rows)} errors={len(err)}',flush=True)
    with (args.output/'strings.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(all_rows)
    (args.output/'strings.json').write_text(json.dumps(all_rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    comparison={}
    if args.baseline:
        with (args.baseline/'strings.csv').open(encoding='utf-8-sig',newline='') as f:old=list(csv.DictReader(f))
        old_spans={(r['file'],int(r['start_byte']),int(r['end_byte'])) for r in old}
        new_spans={(r['file'],r['start_byte'],r['end_byte']) for r in all_rows}
        comparison=dict(baseline_count=len(old),baseline_spans_missing=len(old_spans-new_spans),
                        new_spans=len(new_spans-old_spans),
                        missing_examples=sorted(old_spans-new_spans)[:50],
                        added_examples=sorted(new_spans-old_spans)[:50])
    report=dict(batch='CPP-PILOT-002',files=files,errors=errors,total=len(all_rows),
                unique=len({r['literal'] for r in all_rows}),
                classification_counts=dict(Counter(r['classification'] for r in all_rows)),
                comparison=comparison,limitations=[
                'Preprocessor branches are preserved as context, not evaluated.',
                'Lexical scanner is a second extraction path; raw-string and macro edge cases require review.',
                'AST call context is heuristic; parse errors can reduce context accuracy.',
                'No translation catalog or source edits are produced.'])
    (args.output/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('total','unique','classification_counts','comparison')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
