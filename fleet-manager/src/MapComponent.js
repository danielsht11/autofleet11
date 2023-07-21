import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Polygon, FeatureGroup, Marker, Popup } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import axios from "axios";
import { Modal, Button } from "react-bootstrap";
import { divIcon } from 'leaflet';


const defaultPosition = [51.505, -0.09];

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
    setPolygon(null);
  }

  const vehicleIcon = divIcon({
    html: '🚙',
    className: 'vehicle-icon',
  });

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
              <Marker key={index} position={[vehicle.lat, vehicle.lng]} icon={vehicleIcon}>
                <Popup>
                  <span>Vehicle ID: {vehicle.id}</span>
                </Popup>
              </Marker>
           ))}
        </MapContainer>
      </div>
      <Modal show={modalIsOpen} onHide={handleModalClose}>
        <Modal.Header closeButton>
          <Modal.Title>Vehicles Ids in Selected Area</Modal.Title>
        </Modal.Header>
        <Modal.Body style={{maxHeight: '300px', overflowY: 'auto'}}>
          <ul>
            {selectedVehicles.map((vehicle, index) => (
              <li key={index}>{vehicle.id}</li>
            ))}
          </ul>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleModalClose}>Close</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default MapComponent;
