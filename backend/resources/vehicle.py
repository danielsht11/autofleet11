from flask import json, request
from flask.views import MethodView
from flask_smorest import Blueprint
import json
from os import path
from backend.schemas import PlainVehicleSchema, VehicleSchema, PolygonSchema
from backend.root import SITE_ROOT
from shapely import Polygon, Point

blp = Blueprint("Vehicles", "vehicles", description="Operations on vehicles")


def load_json():
    json_dir = path.join(SITE_ROOT, "static/data", "vehicles-location.json")
    try:
        with open(json_dir, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"could not find the {json_dir}")
    except ValueError:
        print("Decoding json has failed!")


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

    @staticmethod
    def filter_vehicles(vehicles: dict, polygon: Polygon, state: str, name: str) -> list:
        def get_filtered_vehicles(vehicle: dict):

            def _is_vehicle_in_polygon() -> bool:
                lng = vehicle.get("location").get("lng")
                lat = vehicle.get("location").get("lat")
                vehicle_location = Point(lng, lat)

                return vehicle_location.within(polygon)

            def _is_vehicle_matching_filter() -> bool:
                vehicle_state = vehicle.get("state")
                vehicle_name = vehicle.get("class").get("name")

                is_vehicle_match_state = (not state) or vehicle_state == state
                is_vehicle_match_name = (not name) or vehicle_name == name

                return is_vehicle_match_state and is_vehicle_match_name

            return _is_vehicle_in_polygon() and _is_vehicle_matching_filter()

        vehicles_in_polygon = list(filter(get_filtered_vehicles, vehicles))
        return vehicles_in_polygon

    @blp.arguments(PolygonSchema, location="json")
    @blp.response(200, PlainVehicleSchema(many=True))
    def post(self, polygon_data):
        vehicles = load_json()
        coordinates = polygon_data.get('points')
        state = polygon_data.get("state")
        name = polygon_data.get("name")

        polygon_coordinates = self.parse_coordinates(coordinates)
        polygon = Polygon(polygon_coordinates)

        filtered_vehicles = self.filter_vehicles(vehicles, polygon, state, name)
        return filtered_vehicles











