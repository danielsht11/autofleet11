import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";

const FilterComponent = ({ onFilterApply }) => {
  const [stateFilter, setStateFilter] = useState("");
  const [nameFilter, setNameFilter] = useState("");

  const handleFilterApply = () => {
    onFilterApply({ state: stateFilter, name: nameFilter });
  };

  return (
    <Form
      style={{
        position: "absolute",
        bottom: "10px",
        right: "10px",
        zIndex: "1000",
        backgroundColor: "white",
        padding: "10px",
        borderRadius: "10px",
        fontFamily: "Roboto, sans-serif",
      }}
    >
      <Form.Group controlId="formState" style={{ marginBottom: "10px" }}>
        <Form.Label>Filter by State:</Form.Label>
        <Form.Control
          as="select"
          value={stateFilter}
          onChange={(e) => setStateFilter(e.target.value)}
        >
          <option value="">All</option>
          <option value="online">Online 🟢</option>
          <option value="in-ride">In ride 🚥</option>
          <option value="issues">Issues ⚠️</option>
        </Form.Control>
      </Form.Group>
      <Form.Group controlId="formName" style={{ marginBottom: "10px" }}>
        <Form.Label>Filter by Name:</Form.Label>
        <Form.Control
          as="select"
          value={nameFilter}
          onChange={(e) => setNameFilter(e.target.value)}
        >
          <option value="">All</option>
          <option value="A">Motorcycle 🏍️</option>
          <option value="B">Car 🚗</option>
          <option value="C">Truck 🚛</option>
          <option value="D">Bus 🚌</option>
          <option value="E">Trailer 🚚</option>
        </Form.Control>
      </Form.Group>
      <Button variant="primary" onClick={handleFilterApply}>
        Apply Filters
      </Button>
    </Form>
  );
};

export default FilterComponent;
