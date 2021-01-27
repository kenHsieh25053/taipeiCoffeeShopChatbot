from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .. import db


class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True)
    name = db.Column(db.String(20))
    address = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    open_hour = db.Column(db.String(20))
    close_date = db.Column(db.String(10))
    style = db.Column(db.String(30))
    price_level = db.Column(db.String(20))
    space = db.Column(db.String(10))
    plug_number = db.Column(db.String(10))
    comment = db.Column(db.Text)
    map_url = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
