"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *

def get_user_email():
    # Retrieves the current user's email if authenticated
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    # Returns the current UTC time
    return datetime.datetime.utcnow()

# Define the Contact Card table
db.define_table(
    'contact_card',
    Field('user_email', default=get_user_email),  # Associates contact with a specific user
    Field('name', 'string'),  # Contact's name
    Field('affiliation', 'string'),  # Contact's affiliation
    Field('description', 'text'),  # Contact's description or additional details
    Field('photo', 'text', default="https://bulma.io/assets/images/placeholders/96x96.png"),  # Stores photo URL or base64 data
)

db.commit()
