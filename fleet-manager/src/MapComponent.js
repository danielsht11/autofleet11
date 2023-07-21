import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Polygon, FeatureGroup, Marker } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import { EditControl } from "react-leaflet-draw";
import axios from "axios";

const defaultPosition: LatLngExpression = [51.505, -0.09];

const MapComponent = () => {
  const [vehicles, setVehicles] = useState([]); // Define vehicles and setVehicles
  const [polygon, setPolygon] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/vehicles').then(response => {
      setVehicles(response.data); // Update this to use setVehicles
    });
  }, []);

  const handleCreated = (e) => {
    let layer = e.layer; // accessing the layer that was drawn
    let points = layer.getLatLngs(); // getting the coordinates of the polygon
    setPolygon(points[0]); // since getLatLngs() returns multi-dimensional array, take the first array
    axios.post('http://127.0.0.1:5000/vehicles/polygon', points[0]).then(response => {
      setVehicles(response.data); // Update this to use setVehicles
    });
  }

  return (
    <div>
      <div id="map">
        <MapContainer center={defaultPosition} zoom={13} style={{ height: "100vh", width: "100%" }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <FeatureGroup>
            <EditControl
              position="topright"
              onCreated={handleCreated}
              draw={{
                rectangle: false,
                polyline: false,
                circle: false,
                circlemarker: false,
                marker: false
              }}
            />
          </FeatureGroup>
          {polygon && <Polygon positions={polygon} />}
          {vehicles.map((vehicle, index) => (
            <Marker key={index} position={[vehicle.lat, vehicle.lng]} /> // Represent vehicles as markers on the map
          ))}
        </MapContainer>
      </div>
      <div>
        <h2>Vehicles in Selected Area:</h2>
        <ul>
          {vehicles.map((vehicle, index) => (
            <li key={index}>Lat: {vehicle.lat}, Lng: {vehicle.lng}</li>
          ))}
        </ul>
      </div>
    </div>
  );

};

export default MapComponent;
