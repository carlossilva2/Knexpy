# Count

## .count(column: str = "*")

`column`: Which column should it count data. Defaults to `*`

Return a column with the count of the row results.

```python
db = Knex("<db name>")

db.select(
    db.count("id")
).from_("<table>").where("field", "=", "abc")
```

```python
db = Knex("<db name>")

db.select(
    [db.count("id"), "idCount"]
).from_("<table>").where("field", "=", "abc")
```
