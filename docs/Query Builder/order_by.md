# Order by

## .order_by(column: str, order: str = "ASC")

`column`: Name of the column to sort by

`order` (optional): Sets the order of the rows **ASC** for Ascending order, **DESC** for Descending order. Defaults to **ASC**

Order the reulting rows by the value on the provided `column`

```python
db = Knex("<db name>")

db.select().from_("<table>").where("field", "=", "abc").order_by("id")
```

```python
db = Knex("<db name>")

db.select().from_("<table>").where("field", "=", "abc").order_by("id", "DESC")
```
