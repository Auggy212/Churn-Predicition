import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import PredictionForm from './pages/PredictionForm';
import Analytics from './pages/Analytics';
import ModelInfo from './pages/ModelInfo';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/predict" element={<PredictionForm />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/model-info" element={<ModelInfo />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 