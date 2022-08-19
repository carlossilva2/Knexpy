# Insert JSON

## .insert_json(table: str, data: dict | list[dict])

`table`: Table to insert data in

`data`: Can be a single JSON object or a list of JSON objects

Creates a transaction to insert a JSON object. The object will be deconstructed to its key value pair and execute a normal insert statement.
In case of multiple objects it will use [Insert Many](insert_many.md) API.

> **CAUTION**: Object Key is the column name and the json structure should only be of level 1 depth

```python
db = Knex("<db name>")

db.insert_json("<table>", {
    "field": 123,
})

db.insert_json("<table>", [
    {
        "field": 1,
    },
    {
        "field": 2,
    }
])
```
