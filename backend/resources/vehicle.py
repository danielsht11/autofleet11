from flask.views import MethodView
from flask_smorest import Blueprint
from backend.schemas import PlainVehicleSchema, VehicleSchema, PolygonSchema
from shapely import Polygon
from .router import db_session


blp = Blueprint("Vehicles", "vehicles", description="Operations on vehicles")


@blp.route("/vehicles")
class Vehicles(MethodView):
    @blp.response(200, VehicleSchema(many=True))
    def get(self):
        return db_session.data


@blp.route("/vehicles/polygon", methods=["POST"])
class VehiclesPolygon(MethodView):
    @blp.arguments(PolygonSchema, location="json")
    @blp.response(200, PlainVehicleSchema(many=True))
    def post(self, polygon_data):
        coordinates = polygon_data.get('points')
        state = polygon_data.get("state")
        name = polygon_data.get("name")

        polygon_coordinates = db_session.parse_coordinates(coordinates)
        polygon = Polygon(polygon_coordinates)

        filtered_vehicles = db_session.filter_vehicles(db_session.data, polygon, state, name)
        return filtered_vehicles











