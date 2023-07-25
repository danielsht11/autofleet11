import { BrowserRouter as Router, Route, Navigate, Routes } from 'react-router-dom';
import MapComponent from "./MapComponent";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/autofleet-dashboard" element={<MapComponent />} />
        <Route path="/" element={<Navigate to="/autofleet-dashboard" />} />
      </Routes>
    </Router>
  );
}

export default App;
