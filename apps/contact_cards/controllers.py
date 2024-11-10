from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from .models import get_user_email

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    # Main index action to provide URLs for frontend interactions
    return dict(
        get_contacts_url=URL('get_contacts'),
        add_contact_url=URL('add_contact'),
        update_contact_url=URL('update_contact'),
        delete_contact_url=URL('delete_contact'),
        upload_image_url=URL('upload_image'),
    )

@action('get_contacts')
@action.uses(db, auth.user)
def get_contacts():
    # Retrieves all contacts associated with the current user
    user_email = get_user_email()
    contacts = db(db.contact_card.user_email == user_email).select().as_list()
    return dict(contacts=contacts)

@action('add_contact', method="POST")
@action.uses(db, auth.user)
def add_contact():
    # Adds a new contact associated with the current user
    user_email = get_user_email()
    new_contact_id = db.contact_card.insert(
        user_email=user_email,
        name="",
        affiliation="",
        description="",
        photo="https://bulma.io/assets/images/placeholders/96x96.png"
    )
    db.commit()  # Commit changes to the database
    new_contact = db.contact_card[new_contact_id]
    return dict(contact=new_contact.as_dict())

@action('update_contact', method="POST")
@action.uses(db, auth.user)
def update_contact():
    # Updates a specific field for a contact if the current user is authorized
    user_email = get_user_email()
    contact_id = int(request.json.get("id"))
    field = request.json.get("field")
    value = request.json.get("value")

    contact = db.contact_card[contact_id]
    if contact and contact.user_email == user_email:
        if field in ["name", "affiliation", "description"]:
            contact.update_record(**{field: value})
            db.commit()
            return dict(success=True)
    return dict(success=False)

@action('delete_contact', method="POST")
@action.uses(db, auth.user)
def delete_contact():
    # Deletes a contact if the current user is authorized
    user_email = get_user_email()
    contact_id = int(request.json.get("id"))

    contact = db.contact_card[contact_id]
    if contact and contact.user_email == user_email:
        db(db.contact_card.id == contact_id).delete()
        db.commit()  # Commit changes to the database
        return dict(success=True)
    return dict(success=False)

@action('upload_image', method="POST")
@action.uses(db, auth.user)
def upload_image():
    # Handles image upload for a contact, ensuring only the owner can update
    user_email = get_user_email()
    contact_id = int(request.json.get("id"))
    image_data = request.json.get("image")

    contact = db.contact_card[contact_id]
    if contact and contact.user_email == user_email:
        contact.update_record(photo=image_data)
        db.commit()
        return dict(success=True)
    return dict(success=False)
