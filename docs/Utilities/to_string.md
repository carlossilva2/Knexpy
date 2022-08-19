# To String

## .to_string(colorize: bool = False)

`colorize` (optional): Makes output of string somewhat parsed and with colors for operators

Transforms stored query into a single SQL statement

```python
from Knexpy import Knex

db = Knex("<db name>")

query = db.select("field").from_("<table>").where("id", "=", "1")

print(query.to_string())
# SELECT field FROM <table> WHERE id = "1"
```
