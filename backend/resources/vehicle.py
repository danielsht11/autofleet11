from flask import json, request
from flask.views import MethodView
from flask_smorest import Blueprint
import json
from os import path
from backend.schemas import PlainVehicleSchema, VehicleLocationSchema
from backend.root import SITE_ROOT
from shapely import Polygon, Point

blp = Blueprint("Vehicles", "vehicles", description="Operations on vehicles")


def load_json():
    json_dir = path.join(SITE_ROOT, "static/data", "vehicles-location.json")
    with open(json_dir, 'r') as json_file:
        data = json.load(json_file)
        return data


@blp.route("/vehicles")
class Vehicles(MethodView):
    @blp.response(200, VehicleLocationSchema(many=True))
    def get(self):
        vehicles = load_json()
        return vehicles


@blp.route("/vehicles/polygon")
class VehiclesPolygon(MethodView):
    @staticmethod
    def parse_coordinates(coordinates: dict):
        return [(coord.get("location").get("lng"), coord.get("location").get("lat")) for coord in coordinates]

    @blp.response(200, PlainVehicleSchema(many=True))
    def post(self):
        vehicles = load_json()
        coordinates = request.get_json()

        polygon_coordinates = self.parse_coordinates(coordinates)
        polygon = Polygon(polygon_coordinates)

        def get_vehicles_in_polygon(vehicle: dict):
            lng = vehicle.get("location").get("lng")
            lat = vehicle.get("location").get("lat")

            vehicle_location = Point(lng, lat)
            if vehicle_location.within(polygon):
                return True
            return False

        vehicles_in_polygon = list(filter(get_vehicles_in_polygon, vehicles))
        return vehicles_in_polygon










