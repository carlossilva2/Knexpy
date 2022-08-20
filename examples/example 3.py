from pprint import pprint

from Knexpy import Knex

db = Knex("Example_DB", type_check=True)

subquery = db.subquery().select("id").from_("c").where("field", "=", 2000)

update = db.update("t", ["field"], ["Lorem Ipsum Dolor Sit Amet"]).where(
    "field4", "=", subquery
)
update.execute()

query = (
    db.select("id", "field", "field2", "field3")
    .from_("t")
    .where("field4", "=", subquery)
    .order_by("id")
)

results = query.query()

pprint(results)
