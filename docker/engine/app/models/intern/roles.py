from engine.app.models import db
from .default import DefaultModel


class Roles(DefaultModel, db.Model):
    __tablename__ = 'roles'

    role_name = db.Column(db.String(50), unique=True, nullable=False)

    def serialized(self):
        return dict(
            id=self.id,
            role_name=self.role_name,
            created_at=self.created_at
        )

