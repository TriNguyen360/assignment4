"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


# Define the Contact Card table
db.define_table(
    'contact_card',
    Field('user_email', default=get_user_email),  # Email to associate the contact with a specific user
    Field('name', 'string', requires=IS_NOT_EMPTY()),  # Name of the contact
    Field('affiliation', 'string'),  # Affiliation of the contact
    Field('description', 'text'),  # Description field
    Field('photo', 'text', default="https://bulma.io/assets/images/placeholders/96x96.png"),  # Image URL or base64 string
)

db.commit()
