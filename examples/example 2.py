from pprint import pprint

from Knexpy import Knex

db = Knex("Example_DB", type_check=True)


query = (
    db.select("id", ["field", "Lorem"], "field2", "field3")
    .from_("t")
    .where("field4", "=", db.subquery().select("id").from_("c").where("field", "=", 200))
    .order_by("id")
)

results = query.query()

pprint(results)
