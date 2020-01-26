# We're going to import everything for now and do some cleanup after
# from mongoengine import *
from mongoengine import Document
from mongoengine import DynamicDocument
from mongoengine.connection import connect
from mongoengine.fields import StringField
from mongoengine.fields import EmailField
from mongoengine.fields import BinaryField
from mongoengine.fields import IntField
from mongoengine.fields import ListField
from mongoengine.fields import BooleanField
from mongoengine.fields import BooleanField
from mongoengine.fields import DateTimeField
from mongoengine.fields import ReferenceField

from mongoengine.errors import NotUniqueError

from datetime import datetime
import os
import json


# if the database does not exist, it will be created
# connect imported
connect("mongo-dev-db")

# for production:
# connect(
#   db="example-db-name",
#   username="root",
#   password="example123",
#   authentication_source="admin",
#   host="localhost",
#   port=27017
# )

# Defining documents
# User is a subclass of the Document class
class User(Document):
    # http://docs.mongoengine.org/guide/defining-documents.html#fields
    username = StringField(unique=True, required=True)
    email = EmailField(unique=True)
    password=BinaryField(required=True)
    age = IntField()
    bio = StringField(max_length=100)
    # Will accepet strings
    # categoreis = ListField(StringField())
    categories = ListField()
    admin = BooleanField(default=False)
    registered = BooleanField(default=False)
    date_created = DateTimeField(default=datetime.utcnow)

    @classmethod
    def json(self):
        user_dict = {
            "username": self.username,
            "email": self.email,
            "age": self.age,
            "bio": self.bio,
            "categories": self.categories,
            "admin": self.admin,
            "registered": self.registered
        }
        return json.dumps(user_dict)

    # Create meta information about our document
    # Check out docs for more
    meta = {
        "indexes": ["username", "email"],
        # ordering in descending fashion
        "ordering": ["-date_created"]
    }

# Dynamic documents
# BlogPost will be the name of our collection.
# Rather than pass in a document we are passing in dynamic document.
# We could just throw in a pass (line 80) and leave it as is and whenever we
# create a new instance of the class we can pass it any kind of key
# value arguments and it's going ahead and create a new document within
# the blog post collection. There is no enforced schema like there is here
# in the Document class. It's got pros and cons depending on a use case, but
# it can be really handy to have dynamic document.

class BlogPost(DynamicDocument):
    # pass
    title = StringField()
    content = StringField()
    # Reference field to a user
    # If we have not defimed User schema (line 36-69) that would not work    
    author = ReferenceField(User)
    date_created = DateTimeField(default=datetime.utcnow)

    meta = {
        "indexes": ["title"],
        # ordering in descending fashion
        "ordering": ["-date_created"]
    }

# Save a document

user = User(
    username = "PaulSmith",
    email = "psmith@gmail.com",
    password = os.urandom(16),
    age = 54,
    bio = "More of the same",
    admin = False
).save()

user = User(
    username = "MaryBrown",
    email = "mbrown@gmail.com",
    password = os.urandom(16),
    age = 23,
    bio = "Nobody is perfect",
    admin = False
).save()

user = User(
    username = "TomJones",
    email = "tjones@gmail.com",
    password = os.urandom(16),
    age = 43,
    bio = "Best ever",
    admin = False
).save()

user = User(
    username = "BobDylan",
    email = "bdylan@gmail.com",
    password = os.urandom(16),
    age = 37,
    bio = "Yellow submarine",
    admin = True
).save()

user = User(
    username = "PeterPan",
    email = "ppan@gmail.com",
    password = os.urandom(16),
    age = 32,
    bio = "I'm forever young",
)

user.admin = True
user.registered = True

try:
    user.save()
except NotUniqueError:
    print("Username or email is not unique")

