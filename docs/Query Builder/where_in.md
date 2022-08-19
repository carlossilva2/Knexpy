# Where In

## .where_in(column: str, value: list[Any])

`column`: Name of the Column to filter

`value` A list containing multiple values to search in

Shorthand for .where('id', 'in', values), the .where_in method add a "where in" clause to the query. Note that passing empty list as the value results in a query that never returns any rows.

```python
db = Knex("<db name>")

db.select().from_("<table>").where_in("field", ["abc"])
```
