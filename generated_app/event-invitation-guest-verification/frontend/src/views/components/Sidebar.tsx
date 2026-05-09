import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Sidebar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const isActive = (path: string) => location.pathname === path;

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">M</div>
        <div>
          <strong>Metronix</strong>
          <span>Event Suite</span>
        </div>
      </div>

      <nav className="side-nav">
        <button className={isActive('/') ? 'active' : ''} onClick={() => navigate('/')}>
          <span>Verify</span>
          <small>Guest Authentication</small>
        </button>
        <button className={isActive('/invitation') ? 'active' : ''} onClick={() => navigate('/invitation')}>
          <span>Invitation</span>
          <small>Event Details</small>
        </button>
      </nav>

      <div className="side-footer">
        <p className="side-footer-title">Need help?</p>
        <p className="side-footer-text">
          Contact your event host if your mobile number is not yet verified.
        </p>
      </div>
    </aside>
  );
};

export default Sidebar;
