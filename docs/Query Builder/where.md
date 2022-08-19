# Where

## .where(column: str, operator: str, value: Any, join_type: str = "AND")

```python
db = Knex("<db name>")

db.select().from_("<table>").where("field", "=", "abc")
```

```python
db = Knex("<db name>")

db.select()
    .from_("<table>")
    .where("field", "=", "abc")
    .where("field", "<>", "bac")
    .where("field", "LIKE", "ba%", join_type="OR")
```
