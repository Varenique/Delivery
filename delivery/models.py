from delivery.db import db
import mongoengine_goodjson as gj


class Restaurant(gj.Document):
    name = db.StringField()
    address = db.StringField()
    work_time = db.StringField()
    phone_number = db.StringField()

    def to_json(self):
        return {key: getattr(self, key) for key in ['id', 'name', 'address', 'work_time', 'phone_number']
                if getattr(self, key) is not None}
