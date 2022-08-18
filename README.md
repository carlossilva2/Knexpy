# Knexpy

<a href="https://github.com/carlossilva2/Knexpy/blob/main/LICENSE" target="blank"><img src="https://img.shields.io/github/license/carlossilva2/Knexpy?style=round-square&color=green" alt="Knexpy License" /></a>
[![Downloads](https://pepy.tech/badge/knexpy)](https://pepy.tech/project/knexpy)
[![Supported Versions](https://img.shields.io/pypi/pyversions/knexpy.svg)](https://pypi.org/project/knexpy)
<a href="https://www.buymeacoffee.com/cmsilva" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="23" width="100" style="border-radius:5px" /></a>

A query builder for SQLite3 based on Knexjs

## Features

* Transactions
* Type Checking
* Bulk Insert
* JSON mapping

You can report bugs and discuss feature on the [GitHub issues page](https://github.com/carlossilva2/Knexpy/issues).

## Examples

### Creating a Table

```python
from Knexpy import Knex, Field

db = Knex("<Database File Name/Path>")

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
        Field.varchar("field"), # Default size: 255
        Field.varchar("field2"),
        Field.varchar("field3"),
        Field.foreign_key("field4", "c", "id"),
    ],
    not_exists=False, # IF NOT EXISTS clause. Defaults to True
)
```

> When creating a table the fields `id`, `created_at`, `modified_at` are automatically generated.
> The `id` field is a hash based on the information of the Row

### Basic Select

```python
from Knexpy import Knex

db = Knex("<Database File Name/Path>")

query = (
    db.select("id", "field", "field2", ["field3", "test"],...) # List type on select acts as an alias
    .from_("t")
    .where("field", "=", "12345")
    .order_by("id")
)

query.query() # Returns data as JSON
query.query(False) # Returns data as tuples
```

### Select with Subquery

```python
from Knexpy import Knex

db = Knex("<Database File Name/Path>")

query = (
    db.select("id", "field", "field2", ["field3", "test"],...)
    .from_("t")
    .where("field", "=", "12345")
    .where(
        "field4",
        "=",
        db.subquery().select("id").from_("c").where("field", "=", 12345),
        join_type="OR", # If attribute not present defaults to "AND".
    )
    .order_by("id")
)

query.query() # Returns data as JSON
```

### Insert JSON Data

```python
from Knexpy import Knex

db = Knex("<Database File Name/Path>", type_check=True) # type_check enables type checking (duh) when inserting/updating data

db.insert_json("<table>", {
    "field": "1",
    "field2": "2",
    "field3": "3"
})
```
