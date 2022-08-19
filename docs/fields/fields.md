# Field

## Field(name: str, type: str, params: FieldParameters = { })

The Field class is only used when trying to create a table. It offers presets for the most common types, but can use other types by calling the class instead of the statically defined methods.
Besides the type and name, a few other [parameters](#fieldparameters) can be passed as a JSON object.

## FieldParameters

It's basically a JSON object that specifies the charateristics of the column. Only the necessary parameters can be passed, making it easier to write.

```json
{
    "primary_key": false,
    "null": false,
    "auto_increment": false,
    "unique": false,
}
```

> This is the default object used in case nothing is passed on the methods

## Examples

### Primary Key Varchar

```python
from Knexpy import Field

_ = Field("<name>", "varchar(255)", { "primary_key": True })
```

### Primary Key Not Null Auto Increment Integer

```python
from Knexpy import Field

_ = Field("<name>", "int", { "primary_key": True, "null": True, "auto_increment": True })
```
