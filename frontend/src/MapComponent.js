import React, { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, Polygon, FeatureGroup, Marker, Popup } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import axios from "axios";
import { Modal, Button } from "react-bootstrap";
import { divIcon } from "leaflet";
import "bootstrap/dist/css/bootstrap.min.css";
import FilterComponent from "./FilterComponent";

const defaultPosition = [51.505, -0.09];

const MapComponent = () => {
  const [vehicles, setVehicles] = useState([]);
  const [selectedVehicles, setSelectedVehicles] = useState([]);
  const [polygon, setPolygon] = useState([]);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [filter, setFilter] = useState({ state: "", name: "" });

  const filterRef = useRef(filter);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = () => {
    axios
      .get("http://127.0.0.1:5000/vehicles")
      .then((response) => {
        console.log("Received data:", response.data);
        setVehicles(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  const handleCreated = (e) => {
    let layer = e.layer;
    let points = layer.getLatLngs();
    setPolygon(points[0]);

    const dataToSend = {
      points: points[0],
      state: filterRef.current.state,
      name: filterRef.current.name
    };

    axios.post("http://127.0.0.1:5000/vehicles/polygon", dataToSend).then((response) => {
      setSelectedVehicles(response.data);
      setModalIsOpen(true);
    });
  };

  const handleModalClose = () => {
    setModalIsOpen(false);
    setPolygon(null);
  };

  const iconsByClassName = {
    A: divIcon({
      html: "🏍️",
      className: "vehicle-icon",
    }),
    B: divIcon({
      html: "🚗",
      className: "vehicle-icon",
    }),
    C: divIcon({
      html: "🚛",
      className: "vehicle-icon",
    }),
    D: divIcon({
      html: "🚌",
      className: "vehicle-icon",
    }),
    E: divIcon({
      html: "🚚️️",
      className: "vehicle-icon",
    }),
  };

  const handleFilterApply = (appliedFilter) => {
    setFilter(appliedFilter);
    filterRef.current = appliedFilter;
  };

  const filteredVehicles = vehicles.filter((vehicle) => {
    const stateMatch = filter.state ? vehicle.state === filter.state : true;
    const nameMatch = filter.name ? vehicle.name === filter.name : true;
    return stateMatch && nameMatch;
  });

  return (
    <div style={{ position: "relative", height: "100vh" }}>
      <FilterComponent onFilterApply={handleFilterApply} />
      <img
        src={process.env.PUBLIC_URL + "/icon.png"}
        alt="Static"
        style={{ position: "absolute", bottom: "10px", left: "10px", width: "200px", zIndex: "1000" }}
      />
      <div id="map">
        <MapContainer center={defaultPosition} zoom={13} style={{ height: "100%" }}>
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
                marker: false,
              }}
            />
          </FeatureGroup>
          {polygon && <Polygon positions={polygon} />}
          {filteredVehicles.map((vehicle, index) => {
            const icon = iconsByClassName[vehicle.name];
            return (
              <Marker key={index} position={[vehicle.lat, vehicle.lng]} icon={icon}>
                <Popup className="custom-popup">
                  <div>
                    <b>ID:</b> {vehicle.id}
                  </div>
                  <div>
                  <b>State: </b>
                    {vehicle.state === "online"
                      ? "Online 🟢"
                      : vehicle.state === "in-ride"
                      ? "In ride 🚥"
                      : vehicle.state === "issues"
                      ? "Issues ⚠️"
                      : "Unknown"}
                   </div>
                </Popup>
              </Marker>
            );
          })}
        </MapContainer>
      </div>
      <Modal show={modalIsOpen} onHide={handleModalClose} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Vehicles Ids in Selected Area</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <ul className="list-group">
            {selectedVehicles.map((vehicle, index) => (
              <li key={index} className="list-group-item">
                {vehicle.id}
              </li>
            ))}
          </ul>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleModalClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default MapComponent;
