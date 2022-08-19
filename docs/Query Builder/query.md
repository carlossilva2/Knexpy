# Query

## .query(json: bool = True)

`json` (optional): Return data as JSON. Default to `True`

Executes built query until that point, fetches the data and resets the query to the defaults.

```python
db = Knex("<db name>")

db.select().from_("<table>")

db.query()
```

```python
db = Knex("<db name>")

db.select().from_("<table>")

db.query(False) # Returns the Data in tuple format
```
