from engine.app.models import db

patients_and_roles = db.Table('patient_roles', db.metadata,
                              db.Column('patient_id', db.String(50), db.ForeignKey('patients.id'), nullable=False),
                              db.Column('role_id', db.String(50), db.ForeignKey('roles.id'), nullable=False)
                              )

collaborators_and_roles = db.Table('collaborators_roles', db.metadata,
                                   db.Column('collaborators_id', db.String(50), db.ForeignKey('collaborators.id'),
                                             nullable=False),
                                   db.Column('role_id', db.String(50), db.ForeignKey('roles.id'), nullable=False)
                                   )
