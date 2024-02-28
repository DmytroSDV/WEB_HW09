from datetime import datetime

from mongoengine import Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField, BooleanField, DateTimeField
from bson import ObjectId


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    meta = {"collection": "authors"}

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"collection": "quotes"}
