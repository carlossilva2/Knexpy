# Table

## .table(name: str, fields: list[Field], not_exists: bool = True)

`name`: Name to give the table

`fields`: A list containing all the columns of the table. Use [Field API](../fields/fields.md) to create the fields necessary.

`not_exists` (optional): IF NOT EXISTS clause. Defaults to `True`

Creates a new table on the database, if possible. When using this method it will auto create the primary key field `id`, as well as, the `created_at` and `modified_at` date fields.
The `id` field is an hash map of the provided row data with a SALT.

```python
from Knexpy import Knex, Field

db = Knex("<db name>")

db.table(
    "c",
    [
        Field.integer("field"),
    ],
    not_exists=False,
)

db.table(
    "t",
    [
        Field.varchar("field"),
        Field.varchar("field2"),
        Field.varchar("field3"),
        Field.foreign_key("field4", "c", "id"),
    ],
)
```
