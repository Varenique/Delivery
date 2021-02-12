from marshmallow import Schema, fields, post_load
from delivery.models import Restaurant, User


class RestaurantCreateOrUpdateSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    work_time = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    id = fields.Str(dump_only=True)

    @post_load
    def make_restaurant(self, content, **kwargs):
        return Restaurant(**content)


class UserSchema(Schema):
    login = fields.Str(required=True)
    name = fields.Str()
    phone_number = fields.Str()
    role = fields.Str()
    password = fields.Str(load_only=True)
    id = fields.Str(dump_only=True)

    @post_load
    def make_user(self, content, **kwargs):
        return User(**content)
