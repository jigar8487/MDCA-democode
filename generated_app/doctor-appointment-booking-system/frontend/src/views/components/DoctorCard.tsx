import React from 'react';
import { Doctor } from '../../models/types';

const DoctorCard: React.FC<{ doctor: Doctor; onSelect: (doctor: Doctor) => void }> = ({ doctor, onSelect }) => {
  const availableSlots = doctor.availableSlots.filter(slot => !slot.isBooked);

  return (
    <article className="doctor-card" onClick={() => onSelect(doctor)}>
      <div className="doctor-card-header">
        <div className="avatar">{doctor.name.split(' ').at(-1)?.charAt(0) ?? 'D'}</div>
        <span className="status-pill">{availableSlots.length} slots</span>
      </div>
      <h3>{doctor.name}</h3>
      <p className="specialty">{doctor.specialization}</p>
      <div className="detail-list">
        <span>{doctor.clinic}</span>
        <span>{doctor.location}</span>
        <strong>${doctor.fees}</strong>
      </div>
      <div className="slot-list">
        {availableSlots.length > 0
          ? availableSlots.map(slot => <span key={slot.time}>{slot.time}</span>)
          : <span>No slots available</span>}
      </div>
      <button className="primary-button" type="button">Book Appointment</button>
    </article>
  );
};

export default DoctorCard;