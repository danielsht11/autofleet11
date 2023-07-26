import json
from os import path
from backend.root import SITE_ROOT
from shapely import Polygon, Point


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


class Router:
    def __init__(self):
        self.data = load_json()

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


db_session = Router()