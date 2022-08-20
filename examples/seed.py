from Knexpy import Field, Knex

db = Knex("Example_DB", type_check=True)

# Create 2 related tables
# Relation [c 1<------->n t]
db.table(
    "c",
    [
        Field.integer("field"),
    ],
)

db.table(
    "t",
    [
        Field.varchar("field"),
        Field.varchar("field2"),
        Field.varchar("field3"),
        Field.foreign_key("field4", "c", "id"),
    ],
)

db.insert_json(
    "c",
    [
        {"field": 200},
        {"field": 2000},
    ],
)

# Fetch IDs of each entry
c200 = (
    db.select("id")
    .from_("c")
    .where("field", "=", 200)
    .limit(1)
    .order_by("created_at")
    .query()[0]
)
c2000 = (
    db.select("id")
    .from_("c")
    .where("field", "=", 2000)
    .limit(1)
    .order_by("created_at")
    .query()[0]
)

# Insert dummy data with relations
db.insert_json(
    "t",
    [
        {
            "field": "Lorem_200_1",
            "field2": "ipsum_200_1",
            "field3": "dolor_200_1",
            "field4": c200.get("id"),
        },
        {
            "field": "Lorem_200_2",
            "field2": "ipsum_200_2",
            "field3": "dolor_200_2",
            "field4": c200.get("id"),
        },
        {
            "field": "Lorem_2000_1",
            "field2": "ipsum_2000_1",
            "field3": "dolor_2000_1",
            "field4": c2000.get("id"),
        },
        {
            "field": "Lorem_2000_2",
            "field2": "ipsum_2000_2",
            "field3": "dolor_2000_2",
            "field4": c2000.get("id"),
        },
    ],
)
