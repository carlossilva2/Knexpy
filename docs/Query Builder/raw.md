# Raw

## .raw(sql: str, params: list[Any] = None, json: bool = True)

`sql` SQL statement to execute
`params` (optional): List of values use in case of Insert/Update/Delete
`json` (optional): Return data as JSON. Default to `True`

Executes a manual SQL statement. It will auto generate a transaction if statement is an Update, a Delete or an Insert.

```python
db = Knex("<db name>")

db.raw("SELECT * FROM table t")
```

```python
db = Knex("<db name>")

db.raw("INSERT INTO t(field) VALUES ?", ["1"])
```
