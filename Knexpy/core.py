import logging
import sqlite3
import sys
from hashlib import md5
from sqlite3 import Error
from time import time
from typing import Any, Literal

from builder import Field, Querybuilder


class Knex:
    def __init__(self, db: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        try:
            self.db = sqlite3.connect(f"{db}.db", timeout=3600)
            self.query_builder = Querybuilder(self.logger)
            self.__db_name = db
        except Error as e:
            self.logger.error(e)
            sys.exit(1)

    def __repr__(self) -> str:
        return f'Knex(db="{self.__db_name}.db", query="{self.query_builder.to_string()}", values={self.query_builder.values}'

    def select(self, *args: str | list[str]) -> "Knex":
        self.query_builder.select(*args)
        return self

    def from_(self, table: str | list[str]) -> "Knex":
        self.query_builder.from_(table)
        return self

    def where(
        self,
        column: str,
        operator: Literal["=", "<", "<=", ">", ">=", "IN", "NOT IN", "<>", "LIKE"],
        value: Any,
        join_type: Literal["AND", "OR"] = "AND",
    ) -> "Knex":
        self.query_builder.where(column, operator, value, join_type)
        return self

    def where_in(self, column: str, value: list[Any]) -> "Knex":
        self.query_builder.where_in(column, value)
        return self

    def where_null(self, column: str) -> "Knex":
        self.query_builder.where_null(column)
        return self

    def where_not_null(self, column: str) -> "Knex":
        self.query_builder.where_not_null(column)
        return self

    def limit(self, n: int) -> "Knex":
        self.query_builder.limit(n)
        return self

    def order_by(self, column: str, order: Literal["ASC", "DESC"] = "ASC") -> "Knex":
        self.query_builder.order_by(column, order)
        return self

    def table(
        self, name: str, fields: "list[Field] | list[str]", not_exists: bool = True
    ) -> bool:
        query = self.query_builder.table(name, fields, not_exists)
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            self.logger.info("Successfully created table")
            return True
        except Error as e:
            self.logger.error(e)
            return False

    def to_string(self, colorize: bool = False) -> str:
        return self.query_builder.to_string(colorize)

    def insert(self, table: str, fields: "list[str]", values: list[Any]):
        print(self.query_builder.insert(table, fields, values))
        return None

    def query(self, json: bool = True) -> list[tuple[Any]] | list[dict[str, Any]]:
        try:
            cursor = self.db.cursor()
            cursor.execute(self.query_builder.to_string(), self.query_builder.values)
            keys = [_[0] for _ in [d for d in cursor.description]]
            data = cursor.fetchall()
            self.query_builder.reset()
            if json:
                return self.__to_json(keys, data)
            return data
        except Error as e:
            self.logger.error(e)
            self.query_builder.reset()
            return []

    def subquery(self) -> Querybuilder:
        return Querybuilder(self.logger)

    def raw(self, sql: str, params: list[Any] | None = None, json: bool = True):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql) if params == None else cursor.execute(sql, params)
            keys = [_[0] for _ in [d for d in cursor.description]]
            data = cursor.fetchall()
            if json:
                return self.__to_json(keys, data)
            return data
        except Error as e:
            self.logger.error(e)
            self.query_builder.reset()
            return []

    def __to_json(self, keys: list[str], data: list[tuple[Any]]) -> list[dict[str, Any]]:
        res = []
        for _ in data:
            block = {}
            for i, value in enumerate(_):
                block[keys[i]] = value
            res.append(block)
        return res

    """ def insert(
        self, data: dict, table: str, fields: "list | None" = None, empty: bool = False
    ) -> str:
        return self.__insert(data, table, fields, empty)

    def get_fields(
        self,
        table: str,
        fields: "list[str] | None" = ["*"],
        filter: "list[tuple] | None" = None,
        json: bool = True,
    ) -> list:
        if type(fields) != list or table == "" or table == None:
            return []
        if fields == [] or fields == None:
            fields = ["*"]
        cursor = self.db.cursor()
        s = "WHERE "
        values = []
        if filter != None and type(filter) == list:
            for f in filter:
                values.append(f[2])
                s = f"{s}{f[0]}{f[1]}? {f[3] if len(f)>3 else ''} "
        cursor.execute(
            f"SELECT {','.join(fields)} FROM {table} {'' if filter == None else s}",
            tuple(values),
        )
        _ = cursor.fetchall()
        return (
            _
            if not json
            else self.__to_json(_, table, fields if "*" not in fields else None)
        )

    def __insert(
        self,
        data: "dict|tuple",
        table: str,
        spec_fields: "list | None" = None,
        empty: bool = False,
    ) -> str:
        if type(data) not in [list, tuple]:
            print("Type not supported")
            exit(1)
        temp = None
        if type(data) == dict:
            temp = json.dumps(data)
        else:
            temp = "".join([str(_) for _ in data])
        _id = self.__create_id(temp)
        if type(data) == tuple:
            d = list(data)
            d.insert(0, _id)
            temp = tuple(d)
        obj = self.__build_payload(data, _id) if type(data) == dict else temp
        cursor = self.db.cursor()
        columns = (
            self.__get_columns(table)
            if spec_fields == None or spec_fields == []
            else spec_fields
        )
        if len(obj) != len(columns) and not empty:
            print("Payload size incomplete")
            exit(1)
        cursor.execute(
            f"INSERT INTO {table}{'(' if not empty else ''}{','.join(columns if not empty else [])}{')' if not empty else ''} VALUES({','.join(['?' for _ in range(len(columns))])})",
            obj,
        )
        self.db.commit()
        return _id

    def __create_id(self, data: str) -> str:
        def encrypt(*args, **kwargs):
            "Method to encrypt data"
            if "method" not in kwargs:
                raise AttributeError("You must specify a method to encrypt")
            try:
                method = eval(kwargs["method"])
            except Exception:
                exit(1)
            string = ""
            for item in args:
                string += str(item)
            return method(string.encode("UTF-8")).hexdigest()

        return encrypt(time(), data, method="md5")

    def __get_columns(self, table: str, display: "list | None" = None) -> list:
        if display == None:
            cursor = self.db.cursor()
            cursor.execute(f"PRAGMA table_info({table})")
            ans = [f[1] for f in cursor.fetchall()]
        else:
            ans = display
        return ans """


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] → %(message)s",
        datefmt="%H:%M:%S",
    )
    db = Knex("test")

    """ db.table(
        "c",
        [
            Field.integer("salary"),
        ],
        not_exists=False,
    )
    db.table(
        "t",
        [
            Field.varchar("field"),
            Field.varchar("field2"),
            Field.varchar("wtv"),
            Field.foreign_key("salary", "c", "id"),
        ],
        not_exists=False,
    ) """

    """ query = (
        db.select("id", "field", "field2", ["wtv", "field3"])
        .from_("t")
        .where("field", "=", "1")
        .where(
            "salary",
            "=",
            db.subquery().select("id").from_("c").where("salary", "=", 200),
            join_type="OR",
        )
        .order_by("id")
    ) """
    """ .where("field", "<", 1)

        .limit(1)
        .order_by("field2") """
    # print(query.query(True))
    print(db.insert("t", ["field", "field2", "wtv"], [1, 2, 3]), db.query_builder.values)
