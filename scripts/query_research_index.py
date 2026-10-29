#!/usr/bin/env python3
import json
import re
import sqlite3
import sys
from pathlib import Path

BASE = Path("/workspace/engineering/shared")
JSON_PATH = BASE / "multi-agent-research-index.json"
DB_PATH = BASE / "multi-agent-research-index.db"

def rebuild():
    data = json.loads(JSON_PATH.read_text())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS research_fts")
    c.execute("""
        CREATE VIRTUAL TABLE research_fts USING fts5(
            id, date_published, digest_date, category, title, url, key_findings, applied_rule
        )
    """)
    for e in data.get("entries", []):
        c.execute(
            "INSERT INTO research_fts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                e.get("id", ""),
                e.get("date_published", ""),
                e.get("digest_date", ""),
                e.get("category", ""),
                e.get("title", ""),
                e.get("url", ""),
                e.get("key_findings", ""),
                e.get("applied_rule", ""),
            ),
        )
    conn.commit()
    conn.close()
    print(f"Indexed {len(data.get('entries', []))} entries into {DB_PATH}")

def sanitize_fts_query(raw: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9_.]+", raw)
    if not tokens:
        return '""'
    out = []
    for t in tokens:
        if t.upper() in ("OR", "AND", "NOT"):
            out.append(t.upper())
        else:
            out.append(f'"{t}"')
    # Ensure operators aren't leading/trailing/adjacent
    cleaned = []
    for tok in out:
        if tok in ("OR", "AND", "NOT"):
            if not cleaned or cleaned[-1] in ("OR", "AND", "NOT"):
                continue
        cleaned.append(tok)
    while cleaned and cleaned[-1] in ("OR", "AND", "NOT"):
        cleaned.pop()
    return " ".join(cleaned) if cleaned else '""'

def search(query: str):
    if not DB_PATH.exists():
        rebuild()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fts_q = sanitize_fts_query(query)
    rows = c.execute(
        "SELECT id, date_published, category, title, url, applied_rule FROM research_fts WHERE research_fts MATCH ? ORDER BY rank",
        (fts_q,),
    ).fetchall()
    if not rows and " OR " not in fts_q:
        tokens = [f'"{t}"' for t in re.findall(r"[A-Za-z0-9_.]+", query) if t.upper() not in ("OR", "AND", "NOT")]
        if len(tokens) > 1:
            rows = c.execute(
                "SELECT id, date_published, category, title, url, applied_rule FROM research_fts WHERE research_fts MATCH ? ORDER BY rank",
                (" OR ".join(tokens),),
            ).fetchall()
    conn.close()
    for r in rows:
        print(f"[{r[0]}] ({r[1]}) {r[3]} — {r[4]}\n  Category: {r[2]}\n  Rule: {r[5]}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "--rebuild":
        rebuild()
    else:
        search(" ".join(sys.argv[1:]))
