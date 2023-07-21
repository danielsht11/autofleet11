import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Polygon, FeatureGroup, Marker } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import { EditControl } from "react-leaflet-draw";
import axios from "axios";

const defaultPosition: LatLngExpression = [51.505, -0.09];

const MapComponent = () => {
  const [vehicles, setVehicles] = useState([]);
  const [selectedVehicles, setSelectedVehicles] = useState([]);
  const [polygon, setPolygon] = useState([]);
  const [modalIsOpen, setModalIsOpen] = useState(false);

  useEffect(() => {
      axios.get('http://127.0.0.1:5000/vehicles').then(response => {
      setVehicles(response.data);
    });
  }, []);

  const handleCreated = (e) => {
    let layer = e.layer;
    let points = layer.getLatLngs();
    setPolygon(points[0]);
    axios.post('http://127.0.0.1:5000/vehicles/polygon', points[0]).then(response => {
      setSelectedVehicles(response.data);
      setModalIsOpen(true);
    });
  }

  const handleModalClose = () => {
      setModalIsOpen(false);
      setPolygon([]);
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
            <Marker key={index} position={[vehicle.lat, vehicle.lng]} />
          ))}
        </MapContainer>
      </div>
      {modalIsOpen &&
        <div style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'white',
          padding: '1em',
          zIndex: 1000,
        }}>
          <h2>Vehicles in Selected Area:</h2>
          <ul>
            {selectedVehicles.map((vehicle, index) => (
              <li key={index}>{vehicle.id}</li>
            ))}
          </ul>
          <button onClick={handleModalClose}>Close</button>
        </div>
      }
    </div>
  );
};

export default MapComponent;
