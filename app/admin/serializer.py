from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..chatbot.model import ShopModel, FavoriteModel
from marshmallow import Schema, fields
from marshmallow.validate import Length


class ShopSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ShopModel
        load_instance = True


class FavoriteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteModel
        load_instance = True


class UserSchema(Schema):
    id = fields.UUID(allow_none=True)
    email = fields.Email(request=True)
    password = fields.String(required=True, validate=Length(min=4))
    active = fields.Boolean()
    roles = fields.String()
