#!/usr/bin/env python3
"""Audit English/Korean DCSS description files without modifying source.
Run: python tools/dcss-extractor/scripts/audit_descriptions.py --source source --output tools/dcss-extractor/output/DESC-AUDIT-001
This is a static structural audit, not a runtime/quality certification.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

DELIMITER = re.compile(r"^%%%%[ \t]*$", re.M)
KOREAN = re.compile(r"[가-힣]")
REFERENCE = re.compile(r"<([A-Za-z_][^<>\n]*)>")
PRINTF = re.compile(r"%(?:\d+\$)?[-+ #0]*(?:\d+|\*)?(?:\.(?:\d+|\*))?(?:hh|ll|[hljztL])?[diuoxXfFeEgGaAcspn%]")

def parse(path):
    text = path.read_text(encoding="utf-8-sig")
    parts = DELIMITER.split(text)
    entries = []
    # Prefer explicit %%%% boundaries; comments before a key are ignored.
    for idx, part in enumerate(parts[1:], 1):
        lines = part.splitlines()
        first = next((j for j, s in enumerate(lines) if s.strip() and not s.lstrip().startswith("#")), None)
        if first is None:
            continue
        key = lines[first].strip()
        body = "\n".join(lines[first + 1:]).strip()
        entries.append({"key": key, "body": body, "segment": idx})
    return entries

def count_ref(body):
    return Counter(REFERENCE.findall(body))

def check_file(english, korean, writer):
    en, ko = parse(english), parse(korean)
    ed = {x["key"]: x for x in en}
    kd = {x["key"]: x for x in ko}
    en_count, ko_count = Counter(x["key"] for x in en), Counter(x["key"] for x in ko)
    issues = Counter()
    def issue(kind, key, detail=""):
        issues[kind] += 1
        writer.writerow({"file": english.name, "category": kind, "key": key, "detail": detail})
    for key, num in en_count.items():
        if num > 1: issue("duplicate_english_key", key, str(num))
    for key, num in ko_count.items():
        if num > 1: issue("duplicate_korean_key", key, str(num))
    for key in ed:
        if key not in kd:
            issue("missing_korean_key", key)
            continue
        e, k = ed[key]["body"], kd[key]["body"]
        if not k.strip(): issue("empty_korean_body", key)
        elif not KOREAN.search(k) and len(k) > 15 and "{{" not in k:
            issue("review_no_hangul", key, k[:100].replace("\n", " "))
        # Counts only: translated literal references may be legitimate.
        if len(count_ref(e)) != len(count_ref(k)):
            issue("review_reference_count", key, f"EN={sum(count_ref(e).values())} KO={sum(count_ref(k).values())}")
        if len(PRINTF.findall(e)) != len(PRINTF.findall(k)):
            issue("review_printf_count", key, f"EN={len(PRINTF.findall(e))} KO={len(PRINTF.findall(k))}")
        if e.count("{{") != k.count("{{") or e.count("}}") != k.count("}}"):
            issue("review_lua_delimiter", key, f"EN={e.count('{{')}/{e.count('}}')} KO={k.count('{{')}/{k.count('}}')}")
    for key in kd:
        if key not in ed: issue("extra_korean_key", key)
    return {"file": english.name, "english_entries": len(en), "english_unique_keys": len(ed),
            "korean_entries": len(ko), "korean_unique_keys": len(kd),
            "matched_keys": len(ed.keys() & kd.keys()), "issues": dict(sorted(issues.items()))}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=Path("source"))
    p.add_argument("--output", type=Path, default=Path("tools/dcss-extractor/output/DESC-AUDIT-001"))
    args = p.parse_args()
    base = args.source / "dat" / "descript"
    if not base.is_dir(): p.error(f"Missing description directory: {base}")
    args.output.mkdir(parents=True, exist_ok=True)
    en = sorted(base.glob("*.txt"))
    ko = sorted((base / "ko").glob("*.txt"))
    summary = {"english_file_count": len(en), "korean_file_count": len(ko),
               "missing_korean_files": sorted(set(x.name for x in en)-set(x.name for x in ko)),
               "extra_korean_files": sorted(set(x.name for x in ko)-set(x.name for x in en)),
               "files": []}
    with (args.output / "issues.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file","category","key","detail"])
        writer.writeheader()
        for path in en:
            peer = base / "ko" / path.name
            if peer.is_file(): summary["files"].append(check_file(path,peer,writer))
    summary["totals"] = {
        "english_entries": sum(x["english_entries"] for x in summary["files"]),
        "matched_keys": sum(x["matched_keys"] for x in summary["files"]),
        "korean_entries": sum(x["korean_entries"] for x in summary["files"])}
    issues = Counter()
    for row in summary["files"]: issues.update(row["issues"])
    summary["issue_totals"] = dict(sorted(issues.items()))
    (args.output / "summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="files"},ensure_ascii=False,indent=2))
    if summary["missing_korean_files"]: raise SystemExit(2)

if __name__ == "__main__": main()
