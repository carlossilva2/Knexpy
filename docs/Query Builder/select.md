# Select

## .select(*columns: str | list[str])

Creates a select query, taking an optional array of columns for the query, eventually defaulting to * if none are specified when the query is built. The response of a select call will resolve with an array of objects selected from the database.

```python
db = Knex("<db name>")

db.select("field1", "field2").from_("<table>")

# In case of Column alias

db.select("field1", ["field2", "f"]).from_("<table>") #This will resolve to SELECT field1, field2 as "f" from <table>
```
