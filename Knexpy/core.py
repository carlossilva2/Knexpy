import logging
import sqlite3
from sqlite3 import Error
from typing import Any, Literal

from builder import Field, Querybuilder
from chalk import blue, green, red, yellow
from utils import sqlite_to_native


class Knex:
    def __init__(self, db: str, type_check: bool = False, complete: bool = True) -> None:
        logging.basicConfig(
            level=logging.DEBUG,
            format=f"[{blue('%(levelname)s')}] → %(message)s",
            datefmt="%H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        try:
            self.db = sqlite3.connect(
                f"{db}.db" if (".db" not in db and complete) else db, timeout=3600
            )
            self.query_builder = Querybuilder(self.logger)
            self.__tables = self.__get_tables()
            self.__db_name = db
            self.__type_check = type_check
        except Error as e:
            self.logger.error(e)
            raise Exception(e)

    def __repr__(self) -> str:
        return f'{yellow("Knex")}({green("db")}="{self.__db_name}.db", {green("query")}="{self.query_builder.to_string()}", {green("values")}={self.query_builder.values})'

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
        if len(fields) == 0:
            self.logger.error("No fields were inserted")
            return False
        query = self.query_builder.table(name, fields, not_exists)
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            self.logger.info("Successfully created table")
            self.__tables = self.__get_tables()
            return True
        except Error as e:
            self.logger.error(e)
            return False

    def to_string(self, colorize: bool = False) -> str:
        return self.query_builder.to_string(colorize)

    def insert(
        self, table: str, fields: "list[str]", values: list[Any], multi: bool = False
    ) -> tuple[str, list[Any]] | bool:
        statement = self.query_builder.insert(table, fields, values)
        values = self.query_builder.values
        self.__validate_data(table, fields, values)
        if multi:
            self.query_builder.reset()
            return (statement, values)
        cursor = self.db.cursor()
        try:
            cursor.execute("BEGIN;")
            cursor.execute(statement, values)
            self.db.commit()
            self.query_builder.reset()
            return True
        except Error:
            self.logger.error(f"An error occured when executing: {red(statement)}")
            cursor.execute("ROLLBACK;")
            self.query_builder.reset()
            return False

    def insert_many(self, statements: list[tuple[str, list[Any]]]) -> bool:
        faulty = None
        cursor = self.db.cursor()
        try:
            cursor.execute("BEGIN;")
            for statement in statements:
                faulty = statement
                cursor.execute(statement[0], statement[1])
            self.db.commit()
            return True
        except Error:
            self.logger.error(f"An error occured when executing: {red(faulty)}")
            cursor.execute("ROLLBACK;")
            return False

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
        cursor = self.db.cursor()
        insert_or_update = "INSERT INTO" in sql or "UPDATE" in sql
        try:
            if insert_or_update:
                cursor.execute("BEGIN;")
            cursor.execute(sql) if params == None else cursor.execute(sql, params)
            if insert_or_update:
                self.db.commit()
            data = cursor.fetchall()
            if json:
                if len(data) == 0 or cursor.description == None:
                    return {}
                keys = [_[0] for _ in [d for d in cursor.description]]
                return self.__to_json(keys, data)
            return data
        except Error as e:
            if insert_or_update:
                cursor.execute("ROLLBACK;")
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

    def __get_tables(self) -> dict[str, dict[str, Any]]:
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM sqlite_master where type='table'")
            data = cursor.fetchall()
            block = {}
            for table in data:
                block[table[1]] = self.__get_columns(cursor, table[1])
            return block
        except Error as e:
            self.logger.error(e)
            return {}

    def __get_columns(self, cursor: sqlite3.Cursor, table: str) -> dict[str, Any] | None:
        try:
            cursor.execute(f"PRAGMA table_info({table})")
            data = cursor.fetchall()
            block = {}
            for field in data:
                block[field[1]] = sqlite_to_native(field[2])
            return block
        except Error as e:
            self.logger.error(e)

    def __validate_data(self, table: str, fields: list[str], data: list[Any]) -> None:
        if self.__type_check:
            result = True
            f = self.__tables[table]
            keys = f.keys()
            for i, _ in enumerate(fields):
                if _ not in keys:
                    result = False
                    break
                if type(data[i]) != f[_]:
                    result = False
                    break
            if not result:
                raise TypeError("One or more values inserted do not match column type")


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
    """ db.insert_many(
        [
            db.insert(
                "t", ["field", "field2", "wtv", "salary"], [24, 25, 26, 1], multi=True
            ),
            db.insert("t", ["field", "field2", "wtv"], [24, 25, 26], multi=True),
            db.insert(
                "t", ["field", "field2", "wtv", "salary"], [9, 10, 11, 1], multi=True
            ),
            db.insert(
                "t", ["field", "field2", "wtv", "salary"], [12, 13, 14, 2], multi=True
            ),
            db.insert(
                "t", ["field", "field2", "wtv", "salary"], [15, 16, 17, 2], multi=True
            ),
            db.insert(
                "t", ["field", "field2", "wtv", "salary"], [18, 19, 20, 2], multi=True
            ),
        ]  # type: ignore
    ) """
    # db.insert("t", ["field", "field2", "wtv", "salary"], [21, 22, 23, 1])
    """ db.raw(
        "INSERT INTO t(id, field, field2, wtv, salary, created_at, modified_at) VALUES ('asdasdasdasdasdqdfqdqdqdqdqd', 0, 0, 0, 1, '1658773456.9365008', '1658773456.9365008');",
        json=True,
    ) """
