# Execute

## .execute()

Executes stored transaction (Update/Delete) and resets the Query Builder.

```python
db = Knex("<db name>")

db.update("<table>", "field", ["1"]).where("id", "=", "12345")

db.execute()
```
