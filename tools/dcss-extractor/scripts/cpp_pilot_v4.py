"""CPP-PILOT-004: conservative triage of CPP-PILOT-003 (no source edits)."""
import argparse,csv,json,re,collections
from pathlib import Path
OUTPUT={'mpr','mprf','cprintf','yesno','yesnoquit','prompt_for_quantity','prompt_for_int'}
FORMATTING={'make_stringf','stringf','make_stringf2'}
MARKERS={'[SPELL_LIST_BEGIN]','[SPELL_LIST_END]'}
def classify(r,data):
    a=int(r['start_byte'])
    prefix=data[data.rfind(b'\n',0,a)+1:a].decode('utf-8','replace')
    literal=r['literal']; call=r['call_expression'].strip()
    simple=re.split(r'::|\.|->',call)[-1]
    if re.match(r'^\s*#\s*include\s*$',prefix):return 'internal_confirmed','cpp_include_path'
    if literal.strip('"') in MARKERS:return 'internal_confirmed','control_marker'
    if re.match(r'^\s*#\s*(?:if|ifdef|ifndef|elif|define|pragma|error|line)\b',prefix):return 'review_preprocessor','preprocessor_string'
    if simple in OUTPUT and r['context_kind']=='call':return 'visible_direct_candidate','direct_output_call'
    if simple in FORMATTING and r['context_kind']=='call':return 'review_format_result','format_result_needs_consumer'
    if r['context_kind']=='assignment':return 'review_assignment','assigned_string_needs_use_trace'
    if r['context_kind']=='none':return 'review_unresolved','unresolved_ast_context'
    if r['context_kind']=='call':return 'review_call','other_call_needs_semantic_review'
    return 'review_other','unclassified'
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--pilot',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    with (a.pilot/'strings.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    sources={name:(a.source/name).read_bytes() for name in {r['file'] for r in rows}}
    out=[];counts=collections.Counter()
    for r in rows:
        data=sources[r['file']];start=int(r['start_byte']);end=int(r['end_byte'])
        if data[start:end].decode('utf-8','replace')!=r['literal']:raise SystemExit('Offset mismatch: '+r['file']+':'+str(start))
        status,reason=classify(r,data)
        begin=data.rfind(b'\n',0,start)+1;stop=data.find(b'\n',end)
        if stop<0:stop=len(data)
        snippet=data[begin:stop].decode('utf-8','replace').strip()[:240]
        out.append({**r,'phase004_class':status,'phase004_reason':reason,'source_line_snippet':snippet})
        counts[status]+=1
    a.output.mkdir(parents=True,exist_ok=True)
    with (a.output/'strings.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    (a.output/'summary.json').write_text(json.dumps({'batch':'CPP-PILOT-004','total':len(out),'counts':dict(counts),'limitations':['Conservative classification, not full dataflow.','Direct output candidates need verification.','Only include paths and known markers are confirmed internal.']},ensure_ascii=False,indent=2),encoding='utf-8')
    for category in ('review_unresolved','review_assignment','review_format_result','review_call'):
        items=[r for r in out if r['phase004_class']==category]
        with (a.output/(category+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(items)
    print(dict(counts))
if __name__=='__main__':main()
