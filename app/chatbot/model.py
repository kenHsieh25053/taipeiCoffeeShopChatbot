from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .. import db


class ShopModel(db.Model):
    __tablename__ = 'shop'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    open_hour = db.Column(db.String(256))
    close_date = db.Column(db.String(20))
    style = db.Column(db.String(30))
    price_level = db.Column(db.String(30))
    space = db.Column(db.String(20))
    plug_number = db.Column(db.String(20))
    comment = db.Column(db.Text)
    map_url = db.Column(db.String(256))
    facebook = db.Column(db.String(256))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, name, address, latitude, longitude, open_hour, close_date, style, price_level, space, plug_number, comment, map_url, facebook):
        self.id = id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.open_hour = open_hour
        self.close_date = close_date
        self.style = style
        self.price_level = price_level
        self.space = space
        self.plug_number = plug_number
        self.comment = comment
        self.map_url = map_url
        self.facebook = facebook


class FavoriteModel(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True)
    user_id = db.Column(db.String(50))
    shop = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user_id, shop):
        self.user_id = user_id
        self.shop = shop
