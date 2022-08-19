# Insert

## .insert(table: str, fields: list[str], values: list[Any], multi: bool = False)

`table`: Table name

`fields`: Name of the fields where values should go to

`values`: List of values to insert

`multi` (optional): Used only to make the insert statement a Bulk Insert. Check [Insert Many](insert_many.md)

Execute an insert statement by auto performing a transaction. If the `multi` flag is set to True, then the method does not create a transaction and instead returns the raw SQL statement to be used in the [Insert Many](insert_many.md) method.

```python
db = Knex("<db name>")

db.insert("<table>", ["field"], ["1"])
```

> **WARNING**:
> Insert will auto create the row `id` by default, as well as, the `created_at` and `modified_at` fields
