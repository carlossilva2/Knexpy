import sys
from logging import Logger
from sqlite3 import Error
from typing import Any, Literal, TypedDict

import chalk


class FieldParameters(TypedDict, total=False):

    primary_key: bool
    null: bool
    auto_increment: bool
    unique: bool


default_params: FieldParameters = {
    "primary_key": False,
    "null": False,
    "auto_increment": False,
    "unique": False,
}


class Field:
    def __init__(
        self,
        name: str,
        type: str,
        params: FieldParameters = default_params,
    ):
        self.name = name
        self.type = type
        self.params = params
        unique = "" if not params["unique"] else "UNIQUE"
        null = "" if params["null"] else "NOT NULL"
        primary_key = "" if not params["primary_key"] else "PRIMARY KEY"
        auto_increment = "" if not params["auto_increment"] else "AUTOINCREMENT"
        self.column = f"{name} {type} {primary_key} {auto_increment} {unique} {null}"
        self.is_foreign_key = False
        self.foreign_template = "FOREIGN KEY({column}) REFERENCES {table}({foreign})"

    @staticmethod
    def integer(name: str, params: FieldParameters = default_params) -> "Field":
        return Field(name, "int", params)

    @staticmethod
    def blob(name: str, params: FieldParameters = default_params) -> "Field":
        return Field(name, "blob", params)

    @staticmethod
    def float(name: str, params: FieldParameters = default_params) -> "Field":
        return Field(name, "float", params)

    @staticmethod
    def double(name: str, params: FieldParameters = default_params) -> "Field":
        return Field(name, "double", params)

    @staticmethod
    def boolean(name: str, params: FieldParameters = default_params) -> "Field":
        return Field(name, "boolean", params)

    @staticmethod
    def date(name: str, params: FieldParameters = default_params) -> "Field":
        return Field(name, "date", params)

    @staticmethod
    def datetime(name: str, params: FieldParameters = default_params) -> "Field":
        return Field(name, "datetime", params)

    @staticmethod
    def varchar(
        name: str,
        size: int = 255,
        params: FieldParameters = default_params,
    ) -> "Field":
        return Field(name, f"varchar({size})", params)

    @staticmethod
    def text(
        name: str,
        params: FieldParameters = default_params,
    ) -> "Field":
        return Field(name, "text", params)

    @staticmethod
    def foreign_key(
        name: str,
        reference_table: str,
        reference_column: str,
        params: FieldParameters = default_params,
    ) -> "Field":
        field = Field.varchar(name, params=params)
        field.is_foreign_key = True
        field.foreign_template = (
            field.foreign_template.replace("{column}", name)
            .replace("{table}", reference_table)
            .replace("{foreign}", reference_column)
        )
        return field


class Querybuilder:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.values = []

        self.__flags = {
            "select": {"chains": 1, "current": 0},
            "from": {"chains": -1, "current": 0},
            "where": {"chains": -1, "current": 0},
            "sort": {"chains": 1, "current": 0},
            "limit": {"chains": 1, "current": 0},
        }
        self.__select = None
        self.__from = None
        self.__where = None
        self.__order = None
        self.__limit = None
        self.__query = "{select} {from} {where} {order} {limit};"
        self.__create = "CREATE TABLE {exists} {table}({columns});"
        self.__insert = "INSERT INTO {table}({columns}) VALUES ({values});"

    def __repr__(self):
        return f'QueryBuilder(query="{self.to_string()}", values={self.values})'

    def select(self, *args: str | list[str]) -> "Querybuilder":
        f = [_ for _ in args]
        if self.__flags["select"]["current"] >= self.__flags["select"]["chains"]:
            return self
        if self.__flags["select"]["current"] == 0 or not self.__select:
            self.__select = "SELECT <fields>"
        else:
            self.__select = f"{self.__select},<fields>"
        for i, arg in enumerate(f):
            if type(arg) == str:
                pass
            elif type(arg) == list:
                if len(arg) != 2:
                    self.logger.error(
                        "For column aliases, 2 arguments are required: [COLUMN, ALIAS]"
                    )
                    raise TypeError(
                        "For column aliases, 2 arguments are required: [COLUMN, ALIAS]"
                    )
                f[i] = f"{arg[0]} as {arg[1]}"
            else:
                self.logger.error("Only Strings or List of Strings are allowed")
                sys.exit(1)
        fields = ", ".join(f)  # type: ignore
        self.__select = self.__select.replace("<fields>", fields)
        self.__flags["select"]["current"] += 1
        return self

    def from_(self, table: str | list[str]) -> "Querybuilder":
        if self.__flags["from"]["current"] == 0 or not self.__select:
            self.__from = "FROM <table>"
        else:
            self.__from = f"{self.__from}, <table>"
        if type(table) == list:
            if len(table) != 2:
                self.logger.error(
                    "For table aliases, 2 arguments are required: [TABLE, ALIAS]"
                )
                raise TypeError(
                    "For table aliases, 2 arguments are required: [TABLE, ALIAS]"
                )
            table = f"{table[0]} {table[1]}"
        self.__from = self.__from.replace("<table>", table)
        # self.__from = f"FROM {table}"
        self.__flags["from"]["current"] += 1
        return self

    def where(
        self,
        column: str,
        operator: Literal[
            "=", "<", "<=", ">", ">=", "IN", "NOT IN", "IS", "IS NOT", "<>", "LIKE"
        ],
        value: Any,
        join_type: Literal["AND", "OR"] = "AND",
    ) -> "Querybuilder":
        subquery_values = []
        if self.__flags["where"]["current"] == 0 or not self.__where:
            self.__where = "WHERE <clause>"
        else:
            self.__where = f"{self.__where} {join_type} <clause>"
        if isinstance(value, Querybuilder):
            subquery_values.append(*value.values)
            value = f"({value.to_string().replace(';','')})"
            for _ in subquery_values:
                self.values.append(_)
        else:
            self.values.append(value)
            value = "?"
        self.__where = self.__where.replace("<clause>", f"{column} {operator} {value}")
        self.__flags["where"]["current"] += 1
        return self

    def where_in(self, column: str, value: list[Any]) -> "Querybuilder":
        if type(value) != list:
            self.logger.error("Value must be of type List")
        self.where(column, "IN", f"({','.join(value)})")
        return self

    def where_null(self, column: str) -> "Querybuilder":
        self.where(column, "IS", "NULL")
        return self

    def where_not_null(self, column: str) -> "Querybuilder":
        self.where(column, "IS NOT", "NULL")
        return self

    def limit(self, n: int) -> "Querybuilder":
        if self.__flags["limit"]["current"] >= self.__flags["limit"]["chains"]:
            return self
        if self.__flags["limit"]["current"] == 0 or not self.__limit:
            self.__limit = "LIMIT <amount>"
        self.__limit = self.__limit.replace("<amount>", f"{n}")
        self.__flags["limit"]["current"] += 1
        return self

    def order_by(
        self, column: str, order: Literal["ASC", "DESC"] = "ASC"
    ) -> "Querybuilder":
        if self.__flags["sort"]["current"] >= self.__flags["sort"]["chains"]:
            return self
        if self.__flags["sort"]["current"] == 0 or not self.__order:
            self.__order = "ORDER BY <column> <order>"
        else:
            self.__order = f"{self.__order}, <column> <order>"
        self.__order = self.__order.replace("<column>", column).replace("<order>", order)
        self.__flags["sort"]["current"] += 1
        return self

    def table(
        self, name: str, fields: "list[Field] | list[str]", not_exists: bool = True
    ) -> str:
        table_create = self.__create
        fields.insert(0, Field.varchar("id", params={"primary_key": True, "null": False}))
        fields = [
            *fields,
            Field.varchar("created_at"),
            Field.varchar("modified_at"),
        ]
        foreign = []
        columns = []
        for field in fields:
            if isinstance(field, Field):
                columns.append(field.column)
                if field.is_foreign_key:
                    foreign.append(field.foreign_template)
            else:
                columns.append(field)
        columns = [*columns, *foreign]
        columns = ", ".join(columns)
        table_create = (
            table_create.replace("{exists}", "IF NOT EXISTS" if not_exists else "")
            .replace("{table}", name)
            .replace("{columns}", columns)
        )
        return table_create

    def insert(self, table: str, fields: "list[str]", values: list[Any]) -> str:
        t_insert = self.__insert
        if len(fields) != len(values):
            raise Error("Values inserted do not match number of fields")
        t_insert = (
            t_insert.replace("{table}", table)
            .replace("{columns}", f"{', '.join(fields)}")
            .replace("{values}", f"{','.join('?' for _ in fields)}")
        )
        self.values = [*self.values, *values]
        return t_insert

    def to_string(self, colorize: bool = False) -> str:
        return self._build_query(colorize)

    def _build_query(self, colorize: bool = False) -> str:
        query = (
            self.__query.replace("{select}", self.__select if self.__select else "")
            .replace("{from}", self.__from if self.__from else "")
            .replace("{where}", self.__where if self.__where else "")
            .replace("{order}", self.__order if self.__order else "")
            .replace("{limit}", self.__limit if self.__limit else "")
        )

        if colorize:
            query = query.replace("SELECT", chalk.yellow("SELECT"))
            query = query.replace("FROM", f'\n{chalk.yellow("FROM")}')
            query = query.replace("WHERE", f'\n{chalk.yellow("WHERE")}')
            query = query.replace("LIMIT", f'\n{chalk.yellow("LIMIT")}')
            query = query.replace("ORDER BY", f'\n{chalk.yellow("ORDER BY")}')

        return query.replace("  ", "")

    def reset(self) -> "Querybuilder":
        for _ in self.__flags.keys():
            self.__flags[_]["current"] = 0
        self.__select = None
        self.__from = None
        self.__where = None
        self.__order = None
        self.__limit = None
        self.__from = None
        self.values = []
        return self
