# Subquery

## .subquery()

To be used only in Where clause. Creates a clean slate instance of the Query Builder to perform subqueries.

```python
db = Knex("<db name>")

db.select("field", "field2")
    .from_("<table>")
    .where("field", "=", "12345")
    .where(
        "field2",
        "=",
        db.subquery().select("id").from_("<table>").where("field", "=", 12345),
        join_type="OR"
    )
```
