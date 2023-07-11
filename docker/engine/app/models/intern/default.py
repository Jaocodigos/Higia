from engine.app.models import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4


def generate_id():
    return str(uuid4())


class DefaultModel(object):

    id = db.Column(db.String(50), primary_key=True, default=generate_id)
    created_at = db.Column(db.DateTime, default=datetime.now(), index=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
