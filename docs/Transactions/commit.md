# Commit

## .commit(cursor: sqlite3.Cursor | None = None)

`cursor` (optional): SQLite3 Cursor

Performs a Commit transaction. If no cursor is provided it will generate a new cursor.

```python
db = Knex("<db name>")
cursor = db.db.cursor()
try:
    db.begin(cursor)
    db.raw("SELECT * FROM <table> WHERE field=?", "1")
    db.commit(cursor)
except Exception as e:
    db.rollback(cursor)
```
