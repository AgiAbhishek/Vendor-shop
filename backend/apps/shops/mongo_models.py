import mongoengine as me

class Shop(me.Document):
    vendor_id = me.IntField(required=True)  # Django User.id
    name = me.StringField(required=True, max_length=255)
    owner_name = me.StringField(required=True, max_length=255)
    business_type = me.StringField(default='', max_length=100)
    latitude = me.FloatField(required=True, min_value=-90, max_value=90)
    longitude = me.FloatField(required=True, min_value=-180, max_value=180)
    created_at = me.DateTimeField(required=True)
    updated_at = me.DateTimeField(required=True)

    meta = {
        'collection': 'shops',   # MongoDB collection name
        'indexes': [
            'vendor_id',
            'business_type',
            {'fields': ['latitude', 'longitude']},
        ],
        'ordering': ['-created_at'],
    }