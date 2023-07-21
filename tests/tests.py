import pytest
from requests import Response
from app import create_app
from resources.vehicle import load_json
import json
from shapely import Point, Polygon


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def vehicles():
    return load_json()


@pytest.fixture
def all_locations(vehicles):
    locations = []
    for vehicle in vehicles:
        location = {
            "lat": vehicle["location"]["lat"],
            "lng": vehicle["location"]["lng"]
        }
        locations.append(location)
    return locations


@pytest.fixture
def polygon_data():
    return [{"location": {'lng': 51.4694976807, 'lat': -0.0493916683}},
            {"location": {'lng': 51.600112915, 'lat': -0.0382433347}},
            {"location": {'lng': 51.4427490234, 'lat': 0.0197566673}}]


@pytest.fixture
def polygon(polygon_data):
    coordinates = [(coord.get("location").get("lng"), coord.get("location").get("lat")) for coord in polygon_data]
    return Polygon(coordinates)

@pytest.fixture
def vehicles_ids_in_polygon(vehicles, polygon):
    vehicles_ids = []
    for vehicle in vehicles:
        lng = vehicle.get("location").get("lng")
        lat = vehicle.get("location").get("lat")

        coordinate = Point(lng, lat)
        if coordinate.within(polygon):
            vehicles_ids.append(vehicle.get("id"))
    return vehicles_ids


def test_get_all_vehicles_location(client, all_locations):
    response: Response = client.get("/vehicles")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == len(all_locations)

    for vehicle_location in all_locations:
        assert vehicle_location in response.json


def test_get_all_ids_in_polygon(client, polygon_data, vehicles_ids_in_polygon):
    response: Response = client.post("vehicles/polygon", json=polygon_data)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == len(vehicles_ids_in_polygon)
    for vehicle_id in vehicles_ids_in_polygon:
        assert vehicle_id in vehicles_ids_in_polygon







