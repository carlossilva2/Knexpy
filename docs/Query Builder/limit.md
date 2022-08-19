# Limit

## .limit(n: int)

`n`: Maximum number of rows to return

Limit the number of results the query should return. Only applicable on [Select](select.md) Operations.

```python
db = Knex("<db name>")

db.select().from_("<table>").where("field", "=", "abc").limit(1)
```
