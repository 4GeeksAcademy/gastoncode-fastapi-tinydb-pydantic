from fastapi import APIRouter, HTTPException
from tinydb import Query

from database import contacts_table
from models import ContactCreate, ContactUpdate


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


def serialize_document(document):
    return {
        "id": document.doc_id,
        **document
    }


@router.post("")

def create_contact(contact: ContactCreate):

    contact_data = contact.model_dump()

    doc_id = contacts_table.insert(contact_data)

    return {
        "id": doc_id,
        **contact_data
    }


@router.get("")

def get_contacts():

    documents = contacts_table.all()

    return [
        serialize_document(document)
        for document in documents
    ]


@router.get("/search")
def search_contacts(
    name: str | None = None,
    city: str | None = None,
    min_age: int | None = None,
):

    ContactQuery = Query()

    condition = None

    if name is not None:
        condition = ContactQuery.name == name

    if city is not None:

        city_condition = ContactQuery.city == city

        condition = (
            city_condition
            if condition is None
            else condition & city_condition
        )

    if min_age is not None:

        age_condition = ContactQuery.age >= min_age

        condition = (
            age_condition
            if condition is None
            else condition & age_condition
        )

    if condition is None:
        documents = contacts_table.all()
    else:
        documents = contacts_table.search(condition)

    return [
        serialize_document(document)
        for document in documents
    ]


@router.get("/{contact_id}")
def get_contact(contact_id: int):

    document = contacts_table.get(
        doc_id=contact_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return serialize_document(document)


@router.patch("/{contact_id}") 
def update_contact(
    contact_id: int,
    contact: ContactUpdate
):

    document = contacts_table.get(
        doc_id=contact_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    changes = contact.model_dump(
        exclude_unset=True
    )

    if changes:
        contacts_table.update(
            changes,
            doc_ids=[contact_id]
        )

    updated_document = contacts_table.get(
        doc_id=contact_id
    )

    return serialize_document(
        updated_document
    )


@router.delete("/{contact_id}")
def delete_contact(contact_id: int):

    document = contacts_table.get(
        doc_id=contact_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    contacts_table.remove(
        doc_ids=[contact_id]
    )

    return {
        "message": "Contact deleted",
        "id": contact_id
    }


