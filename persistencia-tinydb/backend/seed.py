from database import contacts_table
from models import ContactCreate


seed_data = [
    {
        "name": "Ana",
        "email": "ana@mail.com",
        "age": 28,
        "city": "Buenos Aires"
    },
    {
        "name": "Juan",
        "email": "juan@mail.com",
        "age": 34,
        "city": "Cordoba"
    },
    {
        "name": "Maria",
        "email": "maria@mail.com",
        "age": 19,
        "city": "Buenos Aires"
    }
]


validated_contacts = [
    ContactCreate(**item).model_dump()
    for item in seed_data
]


contacts_table.truncate()

contacts_table.insert_multiple(
    validated_contacts
)


print(
    f"Inserted {len(validated_contacts)} contacts"
)