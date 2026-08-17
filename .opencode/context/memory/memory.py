#!/usr/bin/env python3
"""Persistent, local-first memory for the OpenCode Engineering Kit.

Zero-dependency by default: SQLite + FTS5 full-text search with a recency
boost. Optional vector recall via ChromaDB when `chromadb` is installed and
`KIT_MEMORY_VECTOR=1`.

Data lives OUTSIDE the repository (default ~/.local/share/opencode-engineering-kit)
so it is never committed. Activate with KIT_MEMORY=1.

Usage:
  memory.py init
  memory.py save --key <key> [--session <name>] [--kind <kind>] < content.txt
  memory.py get --key <key>
  memory.py search <query> [--limit N] [--session <name>]
  memory.py sessions
  memory.py stats
  memory.py healthcheck
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys

DEFAULT_DB_DIR = os.path.expanduser("~/.local/share/opencode-engineering-kit")
DB_DIR = os.environ.get("KIT_MEMORY_DIR", DEFAULT_DB_DIR)
DB_PATH = os.path.join(DB_DIR, "memory.db")
VECTOR_ENABLED = os.environ.get("KIT_MEMORY_VECTOR", "0") == "1"


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def connect(db_path=DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init(db_path=DB_PATH):
    conn = connect(db_path)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL REFERENCES sessions(id),
            key TEXT NOT NULL,
            content TEXT NOT NULL,
            kind TEXT DEFAULT 'note',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            key, content, content='memories', content_rowid='id'
        );
        CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
            INSERT INTO memories_fts(rowid, key, content)
            VALUES (new.id, new.key, new.content);
        END;
        CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
            INSERT INTO memories_fts(memories_fts, rowid, key, content)
            VALUES ('delete', old.id, old.key, old.content);
        END;
        CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
            INSERT INTO memories_fts(memories_fts, rowid, key, content)
            VALUES ('delete', old.id, old.key, old.content);
            INSERT INTO memories_fts(rowid, key, content)
            VALUES (new.id, new.key, new.content);
        END;
        """
    )
    conn.commit()
    conn.close()
    return db_path


def ensure_session(conn, name):
    row = conn.execute("SELECT id FROM sessions WHERE name = ?", (name,)).fetchone()
    if row:
        conn.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (now(), row["id"]))
        return row["id"]
    cur = conn.execute(
        "INSERT INTO sessions (name, created_at, updated_at) VALUES (?, ?, ?)",
        (name, now(), now()),
    )
    return cur.lastrowid


def save(key, content, session="default", kind="note", db_path=DB_PATH):
    conn = connect(db_path)
    init(db_path)
    session_id = ensure_session(conn, session)
    ts = now()
    conn.execute(
        "INSERT INTO memories (session_id, key, content, kind, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (session_id, key, content, kind, ts, ts),
    )
    conn.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (ts, session_id))
    conn.commit()
    conn.close()
    return {"session": session, "key": key, "kind": kind, "created_at": ts}


def get(key, db_path=DB_PATH):
    conn = connect(db_path)
    row = conn.execute(
        "SELECT m.key, m.content, m.kind, m.created_at, s.name AS session "
        "FROM memories m JOIN sessions s ON s.id = m.session_id "
        "WHERE m.key = ? ORDER BY m.updated_at DESC LIMIT 1",
        (key,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def search(query, limit=10, session=None, db_path=DB_PATH):
    conn = connect(db_path)
    init(db_path)
    params = [query, limit]
    session_clause = ""
    if session:
        session_clause = " AND s.name = ?"
        params.insert(1, session)
    rows = conn.execute(
        f"""
        SELECT m.key, m.content, m.kind, m.created_at, s.name AS session,
               fts.rank
        FROM memories_fts fts
        JOIN memories m ON m.id = fts.rowid
        JOIN sessions s ON s.id = m.session_id
        WHERE memories_fts MATCH ?{session_clause}
        ORDER BY fts.rank ASC, m.updated_at DESC
        LIMIT ?
        """,
        params,
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def sessions(db_path=DB_PATH):
    conn = connect(db_path)
    rows = conn.execute(
        "SELECT name, created_at, updated_at, "
        "(SELECT COUNT(*) FROM memories m WHERE m.session_id = s.id) AS count "
        "FROM sessions s ORDER BY updated_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def stats(db_path=DB_PATH):
    conn = connect(db_path)
    total = conn.execute("SELECT COUNT(*) AS c FROM memories").fetchone()["c"]
    fts_total = conn.execute("SELECT COUNT(*) AS c FROM memories_fts").fetchone()["c"]
    kinds = {r["kind"]: r["c"] for r in conn.execute("SELECT kind, COUNT(*) AS c FROM memories GROUP BY kind")}
    conn.close()
    return {"memories": total, "fts_indexed": fts_total, "kinds": kinds}


def healthcheck(db_path=DB_PATH):
    result = {"db": db_path, "ok": False}
    try:
        conn = connect(db_path)
        init(db_path)
        row = conn.execute("SELECT COUNT(*) AS c FROM memories").fetchone()
        fts = conn.execute("SELECT COUNT(*) AS c FROM memories_fts").fetchone()
        result["memories"] = row["c"]
        result["fts_indexed"] = fts["c"]
        result["fts_consistent"] = row["c"] == fts["c"]
        result["ok"] = True
        conn.close()
    except Exception as exc:  # pragma: no cover
        result["error"] = str(exc)
    if VECTOR_ENABLED:
        try:
            import chromadb  # noqa: F401

            result["vector"] = "chromadb available"
        except ImportError:
            result["vector"] = "chromadb not installed (install or unset KIT_MEMORY_VECTOR)"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="memory.py", description="Local-first persistent memory for the kit"
    )
    parser.add_argument("--db", default=None, help="override database path")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="initialize the database")

    p_save = sub.add_parser("save", help="save a memory (content from stdin)")
    p_save.add_argument("--key", required=True)
    p_save.add_argument("--session", default="default")
    p_save.add_argument("--kind", default="note")

    p_get = sub.add_parser("get", help="fetch a memory by key")
    p_get.add_argument("--key", required=True)

    p_search = sub.add_parser("search", help="full-text search")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=10)
    p_search.add_argument("--session", default=None)

    sub.add_parser("sessions", help="list sessions")

    sub.add_parser("stats", help="memory statistics")

    sub.add_parser("healthcheck", help="verify the memory database")

    args = parser.parse_args(argv)
    db_path = args.db or DB_PATH

    if args.command == "init":
        print(json.dumps({"initialized": init(db_path)}))
    elif args.command == "save":
        content = sys.stdin.read()
        if not content.strip():
            print("error: empty content", file=sys.stderr)
            return 2
        print(json.dumps(save(args.key, content, args.session, args.kind, db_path)))
    elif args.command == "get":
        result = get(args.key, db_path)
        if result is None:
            print(f"no memory for key '{args.key}'", file=sys.stderr)
            return 1
        print(json.dumps(result))
    elif args.command == "search":
        print(json.dumps(search(args.query, args.limit, args.session, db_path)))
    elif args.command == "sessions":
        print(json.dumps(sessions(db_path)))
    elif args.command == "stats":
        print(json.dumps(stats(db_path)))
    elif args.command == "healthcheck":
        print(json.dumps(healthcheck(db_path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
