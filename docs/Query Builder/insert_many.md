# Insert Many

## .insert_many(statements: list[tuple[str, list[Any]]])

`statements`: A list containing tuples with the SQL statement and its values.

Execute bulk inserts with the [Insert](insert.md) API, when the `multi` flag is set to True.
This method creates a single transaction and executes all INSERT statements at once.

```python
db = Knex("<db name>")

db.insert_many(
    [
        db.insert(
            "<table>", ["field"], [24], multi=True
        ),
        db.insert("<table>", ["field"], [24], multi=True),
        db.insert(
            "<table>", ["field"], [9], multi=True
        ),
        db.insert(
            "<table>", ["field"], [12], multi=True
        ),
        db.insert(
            "<table>", ["field"], [15], multi=True
        ),
        db.insert(
            "<table>", ["field"], [18], multi=True
        ),
    ]
)
```
