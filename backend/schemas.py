from marshmallow import Schema, fields


class PlainVehicleSchema(Schema):
    id = fields.Str(dump_only=True)


class VehicleLocationSchema(PlainVehicleSchema):
    lng = fields.Float(attribute="location.lng")
    lat = fields.Float(attribute="location.lat")


class VehicleLocationRequestSchema(Schema):
    x = fields.Float()
    y = fields.Float()

