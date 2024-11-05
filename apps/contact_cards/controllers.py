from py4web import action, request, URL
from .common import db, auth
from .models import get_user_email

@action('index')
@action.uses('index.html', db, auth.user)
def index():
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
    # Fetch only contacts belonging to the logged-in user
    user_email = get_user_email()
    contacts = db(db.contact_card.user_email == user_email).select().as_list()
    return dict(contacts=contacts)

@action('add_contact', method="POST")
@action.uses(db, auth.user)
def add_contact():
    # Add a new contact tied to the logged-in user
    user_email = get_user_email()
    new_contact_id = db.contact_card.insert(
        user_email=user_email,
        name="",
        affiliation="",
        description="",
        photo="https://bulma.io/assets/images/placeholders/96x96.png"
    )
    new_contact = db.contact_card[new_contact_id]
    return dict(contact=new_contact.as_dict())  # Return the contact data tied to the user

@action('update_contact', method="POST")
@action.uses(db, auth.user)
def update_contact():
    # Ensure update is only applied to contacts owned by the logged-in user
    user_email = get_user_email()
    contact_id = request.json.get("id")
    field = request.json.get("field")
    value = request.json.get("value")

    contact = db.contact_card[contact_id]
    if contact and contact.user_email == user_email:
        if field in ["name", "affiliation", "description"]:
            contact.update_record(**{field: value})
            db.commit()  # Save the update
            return dict(success=True)
    return dict(success=False)

@action('delete_contact', method="POST")
@action.uses(db, auth.user)
def delete_contact():
    # Ensure only contacts owned by the logged-in user are deleted
    user_email = get_user_email()
    contact_id = request.json.get("id")

    contact = db.contact_card[contact_id]
    if contact and contact.user_email == user_email:
        db(db.contact_card.id == contact_id).delete()
        db.commit()
        return dict(success=True)
    return dict(success=False)

@action('upload_image', method="POST")
@action.uses(db, auth.user)
def upload_image():
    # Ensure the image update applies only to the logged-in user's contact
    user_email = get_user_email()
    contact_id = request.forms.get("id")
    image_data = request.forms.get("image")

    contact = db.contact_card[contact_id]
    if contact and contact.user_email == user_email:
        contact.update_record(photo=image_data)
        db.commit()
        return dict(success=True)
    return dict(success=False)
