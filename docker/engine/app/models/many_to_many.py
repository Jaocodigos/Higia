from engine.app.models import db

users_and_roles = db.Table('users_roles', db.metadata,
                           db.Column('user_id', db.String(50), db.ForeignKey('users.id'), nullable=False),
                           db.Column('role_id', db.String(50), db.ForeignKey('roles.id'), nullable=False)
                           )
