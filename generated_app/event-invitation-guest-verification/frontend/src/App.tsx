import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './views/components/Sidebar';
import VerifyPage from './views/pages/VerifyPage';
import InvitationPage from './views/pages/InvitationPage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="main-panel">
          <header className="topbar">
            <div>
              <p className="eyebrow">Event Invitation & Guest Verification</p>
              <h1>Secure Guest Access Portal</h1>
            </div>
            <div className="topbar-card">
              <span>Today</span>
              <strong>{new Date().toLocaleDateString()}</strong>
            </div>
          </header>

          <Routes>
            <Route path="/" element={<VerifyPage />} />
            <Route path="/invitation" element={<InvitationPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
};

export default App;
