# Where Not Null

## .where_not_null(column: str)

`column`: Table column name

Search for rows where `column` is not null

```python
db = Knex("<db name>")

db.select().from_("<table>").where_not_null("field")
```
