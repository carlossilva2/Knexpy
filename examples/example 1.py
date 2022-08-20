from pprint import pprint

from Knexpy import Knex

db = Knex("Example_DB", type_check=True)

query = db.select("id").from_("c")

results = query.query()

pprint(results)
