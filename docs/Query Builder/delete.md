# Delete

## .delete(table: str)

`table`: Name of the table where to delete

Delete 1 or more rows from a table

```python
db = Knex("<db name>")

db.delete("<table>").where("id", "IN", ["1", "2", "3"])
db.execute()
```
