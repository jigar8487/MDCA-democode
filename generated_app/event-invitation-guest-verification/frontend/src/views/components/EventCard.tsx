import React from 'react';
import type { Event } from '../../models/types';

interface EventCardProps {
  event: Event;
  guestName?: string;
}

const EventCard: React.FC<EventCardProps> = ({ event, guestName }) => {
  const eventDate = new Date(event.dateTimeUtc);
  const dateLabel = eventDate.toLocaleDateString(undefined, {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  const timeLabel = eventDate.toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <article className="content-card invitation-card">
      <div className="invitation-header">
        <span className="status-pill">Invitation Confirmed</span>
        {guestName && <span className="guest-name">For: {guestName}</span>}
      </div>

      <h2 className="invitation-title">{event.title}</h2>
      <p className="invitation-host">Hosted by {event.host}</p>

      <div className="profile-stats">
        <div>
          <span>Date</span>
          <strong>{dateLabel}</strong>
        </div>
        <div>
          <span>Time</span>
          <strong>{timeLabel}</strong>
        </div>
        <div>
          <span>Venue</span>
          <strong>{event.venue}</strong>
        </div>
        <div>
          <span>Event ID</span>
          <strong>#{event.id}</strong>
        </div>
      </div>

      <div className="invitation-description">
        <p className="eyebrow">About the Event</p>
        <p>{event.description}</p>
      </div>
    </article>
  );
};

export default EventCard;
