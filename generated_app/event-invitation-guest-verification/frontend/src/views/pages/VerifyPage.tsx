import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useGuestVerification from '../../controllers/useGuestVerification';
import StatusMessage from '../components/StatusMessage';

const VerifyPage: React.FC = () => {
  const navigate = useNavigate();
  const { verify, isLoading, status, message } = useGuestVerification();
  const [mobile, setMobile] = useState('');

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!mobile.trim()) return;
    const result = await verify(mobile.trim());
    if (result.status === 'authorized' && result.guest) {
      // Persist the verified guest in sessionStorage so InvitationPage can read it
      sessionStorage.setItem('verifiedGuest', JSON.stringify(result.guest));
      navigate('/invitation');
    }
  };

  return (
    <section className="page-section">
      <div className="section-header">
        <div>
          <p className="eyebrow">Guest Authentication</p>
          <h2>Verify Your Mobile Number</h2>
          <p className="muted">
            Enter the mobile number you registered with to access your event invitation.
          </p>
        </div>
        <div className="metric-card">
          <span>Security</span>
          <strong>Verified Only</strong>
        </div>
      </div>

      <article className="content-card verify-card">
        <form className="form-grid" onSubmit={onSubmit}>
          <label className="form-label" htmlFor="mobile">
            Mobile Number
          </label>
          <input
            id="mobile"
            type="tel"
            placeholder="e.g. +91-9876543210"
            value={mobile}
            onChange={(e) => setMobile(e.target.value)}
            disabled={isLoading}
            autoFocus
          />

          <button type="submit" className="primary-button wide" disabled={isLoading || !mobile.trim()}>
            {isLoading ? 'Verifying...' : 'Verify & Continue'}
          </button>
        </form>

        <StatusMessage status={status} message={message} />

        <div className="hint-block">
          <p className="eyebrow">Demo Hints</p>
          <ul>
            <li>+91-9876543210 -- Verified guest (Annual Gala)</li>
            <li>+91-9765432109 -- Verified guest (Tech Summit)</li>
            <li>+91-9988776655 -- Not verified</li>
            <li>Any other number -- Not authorized</li>
          </ul>
        </div>
      </article>
    </section>
  );
};

export default VerifyPage;
