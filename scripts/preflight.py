from pathlib import Path
import ast, sys
ROOT = Path(__file__).resolve().parents[1]
errors=[]
required=[
    "contracts/intentclearing.py","contracts/clearing_gate.py","README.md","SUBMISSION.md","DEPLOYMENT.md",
    "docs/ARCHITECTURE.md","docs/INVARIANTS.md","docs/THREAT_MODEL.md","tests/direct/test_intentclearing.py"
]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f"missing {rel}")
for rel in ["contracts/intentclearing.py","contracts/clearing_gate.py","tests/direct/test_intentclearing.py","tests/unit/test_static.py"]:
    try: ast.parse((ROOT/rel).read_text(encoding="utf-8"))
    except Exception as exc: errors.append(f"syntax {rel}: {exc}")
if (ROOT/"frontend").exists(): errors.append("frontend must not exist")
scan_files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".md",".py",".yaml",".toml",".txt"} and p.name != "preflight.py"]
text="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in scan_files)
bad_chain = "619" + "97"
if bad_chain in text: errors.append("studio-dev chain reference found")
if errors:
    print("PREFLIGHT FAILED")
    for e in errors: print("-",e)
    sys.exit(1)
print("PREFLIGHT PASS")
