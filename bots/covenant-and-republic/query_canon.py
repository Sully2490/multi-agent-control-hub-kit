#!/usr/bin/env python3
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("/workspace/constitution-bot/founding-canon.db")

def sanitize(raw: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9_.]+", raw)
    if not tokens:
        return '""'
    out = []
    for t in tokens:
        if t.upper() in ("OR", "AND", "NOT"):
            if out and out[-1] not in ("OR", "AND", "NOT"):
                out.append(t.upper())
        else:
            out.append(f'"{t}"')
    while out and out[-1] in ("OR", "AND", "NOT"):
        out.pop()
    return " ".join(out) if out else '""'

def search(q: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fts = sanitize(q)
    rows = c.execute(
        "SELECT id, category, title, author, date, url, significance FROM founding_canon_fts WHERE founding_canon_fts MATCH ? ORDER BY rank",
        (fts,),
    ).fetchall()
    conn.close()
    for r in rows:
        print(f"[{r[0]}] {r[2]} — {r[3]} ({r[4]})\n  Category: {r[1]}\n  URL: {r[5]}\n  Significance: {r[6]}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search(" ".join(sys.argv[1:]))
