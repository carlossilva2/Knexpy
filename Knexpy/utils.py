from hashlib import md5
from time import time
from typing import Type


def uuid(*args: str) -> str:
    "Method to encrypt data"
    string = ""
    for item in args:
        string += str(item)
    string = f"{time()}-{string}"
    return md5(string.encode("UTF-8")).hexdigest()


def sqlite_to_native(t: str) -> Type:
    t = t.lower().split("(")[0]
    t_str = [
        "varchar",
        "text",
        "character",
        "clob",
        "nvarchar",
        "native character",
        "nchar",
        "varying character",
        "character",
        "blob",
        "numeric",
        "decimal",
        "date",
        "datetime",
    ]
    t_int = [
        "int",
        "integer",
        "tinyint",
        "smallint",
        "mediumint",
        "bigint",
        "unsigned big int",
        "int2",
        "int8",
    ]
    t_float = ["real", "double", "double precision", "float"]
    t_bool = ["boolean"]

    if t in t_str:
        return str
    elif t in t_int:
        return int
    elif t in t_float:
        return float
    elif t in t_bool:
        return bool
    else:
        return None
