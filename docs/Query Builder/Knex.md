# Knex

## Knex("path/file", type_check: bool = False, complete: bool = True)

`type_check` Enables/Disables type checking on insert/update using the native Python types
`complete`: Set to `True` to append ".db" to the end of file name. Set to `False` to disable this append.

Creates a connection to the Database, as well as prepares all the logging stuff.
Retrieves all the tables schema information in first hand even if `type_check` is set to False.

```python
from Knexpy import Knex

db = Knex("<db name>")
```

> This Query Builder is only available for SQLite3
