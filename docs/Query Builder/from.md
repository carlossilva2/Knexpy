# From

## .from_(table: str | list[str])

Specifies the table used in the current query.
In case of the provided `table` is of type list it will interpret as table alias

```python
db = Knex("<db name>")

db.select().from_("<table>")
```

### With Table Alias

```python
db = Knex("<db name>")

db.select().from_(["<table>", "t"])
```
