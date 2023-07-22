from marshmallow import Schema, fields


class PlainVehicleSchema(Schema):
    id = fields.Str(dump_only=True)


class VehicleSchema(PlainVehicleSchema):
    lng = fields.Float(attribute="location.lng")
    lat = fields.Float(attribute="location.lat")
    state = fields.Str()
    name = fields.Str(attribute="class.name")
