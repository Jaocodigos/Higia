from engine.app.models import db
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
    def protected_fields(self):
        return []

    @property
    def default_hided_keys(self):
        return ['_sa_instance_state', 'created_at']

    def serialized(self, protected_fields=None) -> dict:
        if protected_fields is None:
            protected_fields = []

        serialize_data = dict()
        if self.id:
            for k in self.__dict__.keys():

                if k in protected_fields or k in self.default_hided_keys:
                    continue

                if isinstance(self.__dict__.get(k), datetime):
                    serialize_data[k] = self.__dict__.get(k).strftime("%d-%m-%Y")

                elif isinstance(self.__dict__.get(k), list):
                    serialize_data[k] = list()
                    for value in self.__dict__.get(k):
                        serialize_data[k].append(value.serialized(value.protected_fields))

                else:
                    serialize_data[k] = self.__dict__.get(k)

        return serialize_data

    def convert_data_to_table(self) -> list:

        serialize_data = list()
        if self.id:

            for k in self.table_content:
                if k in self.__dict__.keys():

                    if isinstance(self.__dict__.get(k), datetime):
                        serialize_data.append(self.__dict__.get(k).strftime("%d/%m/%Y"))
                    else:
                        serialize_data.append(self.__dict__.get(k))

        return serialize_data
