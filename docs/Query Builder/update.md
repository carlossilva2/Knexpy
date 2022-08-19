# Update

## .update(table: str, fields: list[str], values: list[Any], update_modified: bool = True)

`table`: Name of the table to update

`fields`: A list of which fields should be updated

`values`: A list of the values to update to

`update_modified` (optional): If it should update `modified_at` field on the table

Update 1 or more rows from a table

```python
db = Knex("<db name>")

db.update("<table>", ["field", "field2"], [1, 2, 3]).where("id", "IN", ["1", "2", "3"])
db.execute()
```
