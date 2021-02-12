from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from .. import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    roles = db.Column(
        Enum('user', 'superuser', name='roleEnum'), default='user')
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, email, password, active, roles):
        self.id = id
        self.email = email
        self.password = password
        self.active = active
        self.roles = roles

    @property
    def password(self):
        raise AttributeError('password is not readability attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
