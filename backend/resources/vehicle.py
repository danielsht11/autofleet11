from flask import json, request
from flask.views import MethodView
from flask_smorest import Blueprint
import json
from os import path
from backend.schemas import PlainVehicleSchema, VehicleSchema
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
    @blp.response(200, VehicleSchema(many=True))
    def get(self):
        vehicles = load_json()
        return vehicles


@blp.route("/vehicles/polygon", methods=["POST"])
class VehiclesPolygon(MethodView):
    @staticmethod
    def parse_coordinates(coordinates: dict):
        return [(coord.get("lng"), coord.get("lat")) for coord in coordinates]

    @blp.response(200, PlainVehicleSchema(many=True))
    def post(self):
        vehicles = load_json()
        data = request.get_json()
        coordinates, filters = data.get('points'), data.get('filter')
        state, name = filters.get("state"), filters.get("name")

        polygon_coordinates = self.parse_coordinates(coordinates)
        polygon = Polygon(polygon_coordinates)

        def get_vehicles_in_polygon(vehicle: dict):

            def _is_vehicle_in_polygon() -> bool:
                lng = vehicle.get("location").get("lng")
                lat = vehicle.get("location").get("lat")
                vehicle_location = Point(lng, lat)
                return vehicle_location.within(polygon)

            def _is_vehicle_matching_filter() -> bool:
                vehicle_state = vehicle.get("state")
                vehicle_name = vehicle.get("class").get("name")

                is_vehicle_match_state = vehicle_state == state
                is_vehicle_match_name = vehicle_name == name

                if is_vehicle_match_state and is_vehicle_match_name:
                    return True
                elif not state and is_vehicle_match_name:
                    return True
                elif not name and is_vehicle_match_state:
                    return True
                return False

            if _is_vehicle_in_polygon():
                if not state and not name:
                    return True
                return _is_vehicle_matching_filter()
            return False

        vehicles_in_polygon = list(filter(get_vehicles_in_polygon, vehicles))
        return vehicles_in_polygon










