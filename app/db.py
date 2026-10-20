import os, sqlite3
from flask import current_app, g
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
def get_db():
    if "db" not in g:
        p = current_app.config["DATABASE"]
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        c = sqlite3.connect(p)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys = ON;")
        g.db = c
    return g.db
def close_db(_e=None):
    d = g.pop("db", None)
    if d is not None:
        d.close()
def init_db(app):
    p = app.config["DATABASE"]
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    c = sqlite3.connect(p)
    try:
        fh = open(SCHEMA_PATH, encoding="utf-8")
        c.executescript(fh.read())
        fh.close()
        c.commit()
    finally:
        c.close()
def row_to_dict(r):
    return dict(r) if r is not None else None
def rows_to_dicts(rs):
    return [dict(x) for x in rs]

