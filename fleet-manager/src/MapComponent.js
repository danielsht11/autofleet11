import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Polygon, FeatureGroup } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import { EditControl } from "react-leaflet-draw";
import axios from "axios";

const defaultPosition: LatLngExpression = [51.505, -0.09];

const MapComponent = () => {
  const [vehicleIds, setVehicleIds] = useState([]);
  const [polygon, setPolygon] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/vehicles').then(response => {
      setVehicleIds(response.data.map(vehicle => vehicle.id));
    });
  }, []);

  const handleCreated = (e) => {
    let layer = e.layer; // accessing the layer that was drawn
    let points = layer.getLatLngs(); // getting the coordinates of the polygon
    setPolygon(points[0]); // since getLatLngs() returns multi-dimensional array, take the first array
    axios.post('http://127.0.0.1:5000/vehicles/polygon', points[0]).then(response => {
      setVehicleIds(response.data.map(vehicle => vehicle.id));
    });
  }
  return (
    <div>
      <div id="map">  {/* add this id here */}
        <MapContainer center={defaultPosition} zoom={13} style={{ height: "100vh", width: "100%" }}>  {/* and apply inline styles */}
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
        </MapContainer>
      </div>
      <div>
        <h2>Vehicle IDs in Selected Area:</h2>
        <ul>
          {vehicleIds.map((id, index) => (
            <li key={index}>{id}</li>
          ))}
        </ul>
      </div>
    </div>
  );

};

export default MapComponent;
