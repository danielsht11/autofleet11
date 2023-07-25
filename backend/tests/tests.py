import pytest
from requests import Response
from backend.app import create_app
from backend.resources.vehicle import load_json
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
            "id": vehicle.get("id"),
            "lat": vehicle.get("location").get("lat"),
            "lng": vehicle.get("location").get("lng"),
            "state": vehicle.get("state"),
            "name": vehicle.get("class").get("name")
        }
        locations.append(location)
    return locations


@pytest.fixture
def polygon_points():
    return [{
          "lat": 51.50959718054336,
          "lng": -0.09664535522460939},
        {
          "lat": 51.539609109272924,
          "lng": -0.14488220214843753
        },
        {
          "lat": 51.54024971769134,
          "lng": -0.07398605346679689
        },
        {
          "lat": 51.49944632447973,
          "lng": -0.08497238159179688
        }
      ]


@pytest.fixture
def polygon(polygon_points):
    coordinates = [(coord.get("lng"), coord.get("lat"))
                   for coord in polygon_points]
    return Polygon(coordinates)


@pytest.fixture
def vehicles_in_polygon(vehicles, polygon):
    vehicles_in_polygon = []
    for vehicle in vehicles:
        lng = vehicle.get("location").get("lng")
        lat = vehicle.get("location").get("lat")

        coordinate = Point(lng, lat)
        if coordinate.within(polygon):
            vehicles_in_polygon.append(vehicle)
    return vehicles_in_polygon


@pytest.fixture
def vehicles_ids_in_polygon(vehicles_in_polygon):
    return [vehicle.get("id") for vehicle in vehicles_in_polygon]


@pytest.fixture
def state():
    return "online"


@pytest.fixture
def vehicle_class():
    return "B"


@pytest.fixture
def filtered_polygon_vehicles_ids(vehicles_in_polygon, state, vehicle_class):
    filtered_vehicles_ids = []
    for vehicle in vehicles_in_polygon:
        if vehicle.get("state") == state and vehicle.get("class").get("name") == vehicle_class:
            filtered_vehicles_ids.append(vehicle.get("id"))
    return filtered_vehicles_ids


def test_get_all_vehicles_location(client, all_locations):
    response: Response = client.get("/vehicles")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == len(all_locations)

    for vehicle_location in all_locations:
        assert vehicle_location in response.json


def test_get_all_ids_in_polygon(client, polygon_points, vehicles_ids_in_polygon):
    polygon_data = {
        "points": polygon_points,
        "filter": {
            "state": "",
            "name": ""
        }
    }
    response: Response = client.post("vehicles/polygon", json=polygon_data)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == len(vehicles_ids_in_polygon)
    for vehicle in response.json:
        assert vehicle.get("id") in vehicles_ids_in_polygon


def test_get_all_ids_in_filtered_polygon(client, polygon_points, state, vehicle_class, filtered_polygon_vehicles_ids):
    polygon_data = {
        "points": polygon_points,
        "state": state,
        "name": vehicle_class
        }

    response: Response = client.post("vehicles/polygon", json=polygon_data)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == len(filtered_polygon_vehicles_ids)
    for vehicle in response.json:
        assert vehicle.get("id") in filtered_polygon_vehicles_ids




