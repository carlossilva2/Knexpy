# Knex

## Knex(db: str, type_check: bool = False, complete: bool = True)

`db`: Path or File name of the database to use

`type_check`: Enables/Disables type checking on insert/update using the native Python types

`complete` (optional): Set to `True` to append ".db" to the end of file name. Set to `False` to disable this append.

Creates a connection to the Database, as well as prepares all the logging stuff.
Retrieves all the tables schema information in first hand even if `type_check` is set to False.

### Available Properties

`db_tables` -> Dict : Multi depth Dictionary with table name, field names and types

`db` -> sqlite3.Connection : Database connection

`query_builder` -> Querybuilder : Querybuilder instance

`logger` -> logging.Logger : Logging instance

### Example

```python
from Knexpy import Knex

db = Knex("<db name>")
```

> This Query Builder is only available for SQLite3
