
from django.db import models
from django.conf import settings

from datetime import datetime

from mockfirestore import Timestamp


class base_object:
    def __init__(self):
        self.collection = ''
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.uuid: str = None

    def create(self, data):
        db = settings.DEFAULT_APP
        obj = db.collection(self.collection).add(data)
        self.uuid = obj[1].id
        self.created_at = obj[0]    # with nanosecond will see if I need to change it
        self.updated_at = obj[0]    # with nanosecond will see if I need to change it
        for att, value in data.items():
            self.__setattr__(att, value)
        return self, obj

    def update(self, data: dict = None, uuid: str = None):
        db = settings.DEFAULT_APP
        uuid = uuid if self.uuid is None else self.uuid
        print(f"updating user {uuid} | data: {data}")
        if uuid is None:
            raise Exception("No uiid")
        db.collection(self.collection).document(uuid).update(data)
        for att, value in data.items():
            self.__setattr__(att, value)
        return self

    def get_by_email(self, email: str):
        db = settings.DEFAULT_APP

        # I should check the count of the Query's result
        print(f"Users:{db.collection(self.collection).get()}")
        doc = list(db.collection(self.collection).where('email', '==', email).get())[0]
        self.uuid = doc.id
        for att, value in doc.to_dict().items():
            self.__setattr__(att, value)
        return self


class User(base_object):
    def __init__(self):
        super().__init__()
        self.collection = 'users'

        self.email: str = None
        self.password: str = None
        self.is_verified: bool = False
        self.status: str = None
        self.email: str = None

        self.code: int = None
        self.code_end_on: float =None

    def __repr__(self):
        return (
            f'User(\
                uuid={self.uuid}, \
                email={self.email}, \
                password={self.password}, \
                status={self.status}, \
                created_at={self.created_at}\
                updated_at={self.updated_at}\
            )'
        )

    def create(self, data):
        user, _ = super().create(data)
        self.status = "created"
        return self

    def to_json(self):
        d = self.__dict__
        d.pop("password", None)
        for k, v in d.items():
            if isinstance(v, Timestamp):
                d[k] = str(v.seconds)
        return d


class Verification_code(models.Model):
    updated_at = models.DateTimeField(auto_now_add=True)
    user_uuid = models.UUIDField()
    digits = models.TextField()
    end_at = models.DateTimeField()
