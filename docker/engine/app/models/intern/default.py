from engine.app.models import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4


def generate_id():
    return str(uuid4())


class DefaultModel(object):

    id = db.Column(db.String(50), primary_key=True, index=True, default=generate_id)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def default_hided_keys(self):
        return ['_sa_instance_state', 'created_at']

    def serialized(self, protected_fields=[]):
        serialize_data = dict()
        if self.id:
            for k in self.__dict__.keys():
                if k in protected_fields or k in self.default_hided_keys:
                    continue
                if isinstance(self.__dict__.get(k), datetime):
                    serialize_data[k] = self.__dict__.get(k).strftime("%Y-%m-%d")
                else:
                    serialize_data[k] = self.__dict__.get(k)
        else:
            return {}
        return serialize_data
