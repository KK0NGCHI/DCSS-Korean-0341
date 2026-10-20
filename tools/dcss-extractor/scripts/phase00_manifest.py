"""Generate a read-only SHA-256 manifest of the local DCSS 0.34.1 source."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

PILOT = ("message.cc", "invent.cc", "describe.cc", "newgame.cc")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True, help="Path to original source directory")
    ap.add_argument("--output", type=Path, default=Path("config/source-manifest.json"))
    args = ap.parse_args()
    source = args.source.resolve()
    if not (source / "Makefile").is_file():
        ap.error(f"Not a DCSS source directory (missing Makefile): {source}")
    records, errors = [], []
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            data = path.read_bytes()
            records.append({"path": path.relative_to(source).as_posix(), "bytes": len(data),
                            "sha256": hashlib.sha256(data).hexdigest()})
        except OSError as exc:
            errors.append({"path": str(path), "error": str(exc)})
    missing = [p for p in PILOT if not (source / p).is_file()]
    manifest = {"schema_version": 1, "generated_utc": datetime.now(timezone.utc).isoformat(),
                "source_root": str(source), "file_count": len(records),
                "total_bytes": sum(x["bytes"] for x in records),
                "pilot_files_missing": missing, "read_errors": errors, "files": records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest: {args.output} | files: {len(records)} | missing pilot: {len(missing)} | read errors: {len(errors)}")
    if missing or errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
