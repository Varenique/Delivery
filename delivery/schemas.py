from marshmallow import Schema, fields, post_load
from delivery.models import Restaurant


class RestaurantCreateOrUpdateSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    work_time = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    id = fields.Str(dump_only=True)

    @post_load
    def make_restaurant(self, content, **kwargs):
        return Restaurant(**content)
