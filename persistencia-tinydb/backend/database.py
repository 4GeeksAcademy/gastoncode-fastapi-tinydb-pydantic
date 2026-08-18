from tinydb import TinyDB


db = TinyDB("db.json")

contacts_table = db.table("contacts")