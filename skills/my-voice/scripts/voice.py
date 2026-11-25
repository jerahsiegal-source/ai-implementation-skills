#!/usr/bin/env python3
"""my-voice helper. Standard library only.

Commands:
  init                     create the private data folder
  status                   show corpus, samples, profile and edit counts
  import FILES...          convert .docx/.pdf/.txt/.md to labeled samples
  log-edit                 save a before/after edit pair
  snapshot                 copy profile/ to versions/<timestamp>/
  mark-learned             record that edits up to now were processed
  where                    print the data folder path

Data folder: $MY_VOICE_HOME, else ~/.ai-skills/personal/my-voice
(an older ~/.my-voice is used if the default doesn't exist yet).
On Windows run it with `python` or `py`.
"""
import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

LAYOUT = [
    "corpus/samples/docs",
    "profile/mediums",
    "edits",
    "blindtest",
    "versions",
    "evals",
]

SEED_FILES = {
    "rules.md": "# Rules\nHard rules the user has stated. Drafts follow these without exception.\n\n",
    "corpus/samples/index.md": "# Samples index\n\n| File | Count | Years | Channel | Author |\n|---|---|---|---|---|\n",
    ".gitignore": "*\n",
}


def home() -> Path:
    env = os.environ.get("MY_VOICE_HOME")
    if env:
        return Path(env).expanduser()
    default = Path.home() / ".ai-skills" / "personal" / "my-voice"
    legacy = Path.home() / ".my-voice"
    if not default.exists() and legacy.is_dir():
        return legacy
    return default


def now() -> dt.datetime:
    return dt.datetime.now()


def cmd_init(_args):
    h = home()
    for d in LAYOUT:
        (h / d).mkdir(parents=True, exist_ok=True)
    for rel, text in SEED_FILES.items():
        p = h / rel
        if not p.exists():
            p.write_text(text, encoding="utf-8")
    print(f"my-voice data folder ready: {h}")


def words(p: Path) -> int:
    try:
        return len(p.read_text(encoding="utf-8", errors="ignore").split())
    except OSError:
        return 0


def edits_since_learn(h: Path):
    marker = h / "edits" / ".last-learn"
    since = marker.stat().st_mtime if marker.exists() else 0
    return [p for p in (h / "edits").glob("*.md")
            if p.stat().st_mtime > since and not p.name.startswith("setup-")]


def cmd_status(_args):
    h = home()
    if not h.exists():
        print(f"No data folder at {h}. Run: python3 scripts/voice.py init")
        return
    print(f"Data folder: {h}\n")
    print("Corpus")
    for name in ["talk", "habits", "scenarios", "taste", "interview", "scenarios-plus"]:
        p = h / "corpus" / f"{name}.md"
        mark = "x" if p.exists() and words(p) > 20 else " "
        print(f"  [{mark}] {name:<15} {words(p) if p.exists() else 0:>6} words")
    samples = [p for p in (h / "corpus" / "samples").rglob("*.md") if p.name != "index.md"]
    labels = {"typed by me": 0, "ai-assisted": 0, "ai-written": 0, "someone else": 0}
    # "possibly AI-assisted" counts as ai-assisted
    entries = 0
    for p in samples:
        text = p.read_text(encoding="utf-8", errors="ignore")
        heads = re.findall(r"^(?:## .*|<!-- SAMPLE .*)$", text, flags=re.M)
        entries += len(heads)
        for line in heads:
            low = line.lower()
            for k in labels:
                if k in low:
                    labels[k] += 1
    print(f"\nSamples: {len(samples)} files, {entries} pieces, {sum(words(p) for p in samples)} words")
    print("  " + ", ".join(f"{k}: {v}" for k, v in labels.items()))
    base = h / "profile" / "base.md"
    if base.exists():
        age = (now() - dt.datetime.fromtimestamp(base.stat().st_mtime)).days
        print(f"\nProfile: built, last change {age} day(s) ago")
        mediums = sorted(p.stem for p in (h / "profile" / "mediums").glob("*.md"))
        print(f"  mediums: {', '.join(mediums) or 'none'}")
    else:
        print("\nProfile: not built yet")
    print(f"\nEdits since last learn: {len(edits_since_learn(h))}")
    results = sorted((h / "blindtest").glob("*-results.md"))
    if results:
        first = results[-1].read_text(encoding="utf-8", errors="ignore").splitlines()
        score = next((l for l in first if l.lower().startswith("score")), "")
        print(f"Last blind test: {results[-1].stem} {score}")
    else:
        print("Last blind test: never")


def docx_to_text(path: Path) -> str:
    if shutil.which("pandoc"):
        out = subprocess.run(["pandoc", str(path), "-t", "gfm", "--wrap=none"],
                             capture_output=True, text=True)
        if out.returncode == 0:
            return out.stdout
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    paras = []
    for p in root.iter(f"{{{ns['w']}}}p"):
        style = p.find("w:pPr/w:pStyle", ns)
        text = "".join(t.text or "" for t in p.iter(f"{{{ns['w']}}}t"))
        if style is not None and "Heading" in (style.get(f"{{{ns['w']}}}val") or "") and text:
            text = "## " + text
        paras.append(text)
    return "\n\n".join(paras)


def file_to_text(path: Path) -> str:
    suf = path.suffix.lower()
    if suf == ".docx":
        return docx_to_text(path)
    if suf == ".pdf":
        if not shutil.which("pdftotext"):
            sys.exit("pdftotext not found. Install poppler, or paste the text instead.")
        return subprocess.run(["pdftotext", "-layout", str(path), "-"],
                              capture_output=True, text=True).stdout
    if suf in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    sys.exit(f"Unsupported file type: {path.name}")


def cmd_import(args):
    h = home()
    dest = h / "corpus" / "samples" / "docs"
    dest.mkdir(parents=True, exist_ok=True)
    for f in args.files:
        src = Path(f).expanduser()
        text = file_to_text(src)
        name = re.sub(r"[^A-Za-z0-9_.-]+", "_", src.stem) + ".md"
        header = (f"<!-- SAMPLE | {args.year} | {args.channel} | {args.author} | "
                  f"Imported word for word from {src.name}. Prompts or text not written by "
                  f"the user must be wrapped in NOT-MY-WRITING markers. -->\n\n")
        (dest / name).write_text(header + text, encoding="utf-8")
        with open(h / "corpus" / "samples" / "index.md", "a", encoding="utf-8") as idx:
            idx.write(f"| docs/{name} | 1 | {args.year} | {args.channel} | {args.author} |\n")
        print(f"imported {src.name} -> {dest / name} ({len(text.split())} words)")


def read_arg(value):
    if value is None:
        return ""
    p = Path(value).expanduser()
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="ignore")
    return value


def cmd_log_edit(args):
    h = home()
    stamp = now().strftime("%Y-%m-%d-%H%M%S")
    out = h / "edits" / f"{stamp}-{args.medium}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    body = (f"# Edit | {args.medium} | {now():%Y-%m-%d %H:%M}\n\n"
            f"## Before\n\n{read_arg(args.before).strip()}\n\n"
            f"## After\n\n{read_arg(args.after).strip()}\n\n"
            f"## User's words\n\n{(args.note or '').strip()}\n")
    out.write_text(body, encoding="utf-8")
    n = len(edits_since_learn(h))
    print(f"saved {out}")
    if n >= 10:
        print(f"{n} edits since last learn: offer /my-voice learn")


def cmd_snapshot(_args):
    h = home()
    src = h / "profile"
    if not (src / "base.md").exists():
        print("no profile to snapshot")
        return
    dst = h / "versions" / now().strftime("%Y-%m-%d-%H%M%S")
    shutil.copytree(src, dst)
    print(f"snapshot -> {dst}")


def cmd_mark_learned(_args):
    m = home() / "edits" / ".last-learn"
    m.parent.mkdir(parents=True, exist_ok=True)
    m.write_text(now().isoformat(), encoding="utf-8")
    print("marked")


def main():
    ap = argparse.ArgumentParser(description="my-voice helper")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("snapshot").set_defaults(fn=cmd_snapshot)
    sub.add_parser("mark-learned").set_defaults(fn=cmd_mark_learned)
    sub.add_parser("where").set_defaults(fn=lambda a: print(home()))
    imp = sub.add_parser("import")
    imp.add_argument("files", nargs="+")
    imp.add_argument("--year", required=True)
    imp.add_argument("--channel", required=True, help="e.g. report, application, email")
    imp.add_argument("--author", default="typed by me")
    imp.set_defaults(fn=cmd_import)
    le = sub.add_parser("log-edit")
    le.add_argument("--medium", required=True)
    le.add_argument("--before", required=True, help="text or path to a file")
    le.add_argument("--after", required=True, help="text or path to a file")
    le.add_argument("--note", default="")
    le.set_defaults(fn=cmd_log_edit)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
