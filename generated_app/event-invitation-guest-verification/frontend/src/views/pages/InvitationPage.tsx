import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EventCard from '../components/EventCard';
import type { Guest } from '../../models/types';

const InvitationPage: React.FC = () => {
  const navigate = useNavigate();
  const [guest, setGuest] = useState<Guest | null>(null);
  const [confirmed, setConfirmed] = useState(false);

  useEffect(() => {
    const raw = sessionStorage.getItem('verifiedGuest');
    if (!raw) {
      navigate('/');
      return;
    }
    try {
      const parsed: Guest = JSON.parse(raw);
      setGuest(parsed);
    } catch {
      navigate('/');
    }
  }, [navigate]);

  const handleConfirm = () => {
    setConfirmed(true);
  };

  const handleSignOut = () => {
    sessionStorage.removeItem('verifiedGuest');
    navigate('/');
  };

  if (!guest || !guest.event) {
    return <p className="state-card">Loading invitation...</p>;
  }

  return (
    <section className="page-section">
      <div className="section-header">
        <div>
          <p className="eyebrow">Welcome, {guest.name}</p>
          <h2>Your Event Invitation</h2>
          <p className="muted">Review the details below and confirm your attendance.</p>
        </div>
        <button className="secondary-button" onClick={handleSignOut}>
          Sign Out
        </button>
      </div>

      <EventCard event={guest.event} guestName={guest.name} />

      {!confirmed ? (
        <button className="primary-button wide" onClick={handleConfirm}>
          Confirm Attendance
        </button>
      ) : (
        <div className="state-card success">
          Thank you, {guest.name}. Your attendance has been confirmed. We look forward to seeing you at {guest.event.title}.
        </div>
      )}
    </section>
  );
};

export default InvitationPage;
