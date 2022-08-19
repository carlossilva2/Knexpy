# Where Null

## .where_null(column: str)

`column`: Table column name

Search for rows where `column` is null

```python
db = Knex("<db name>")

db.select().from_("<table>").where_null("field")
```
