import React from 'react';
import { Booking } from '../../models/types';

interface AppointmentRowProps {
  appointment: Booking;
  onApprove: (bookingRef: string) => void;
  onCancel: (bookingRef: string) => void;
}

const AppointmentRow: React.FC<AppointmentRowProps> = ({ appointment, onApprove, onCancel }) => {
  return (
    <tr>
      <td>{appointment.reference}</td>
      <td>{appointment.patientName}</td>
      <td>{appointment.mobile}</td>
      <td>{appointment.email}</td>
      <td>{appointment.slot}</td>
      <td>{new Date(appointment.appointmentDate).toLocaleDateString()}</td>
      <td><span className={`status-badge ${appointment.status}`}>{appointment.status}</span></td>
      <td className="table-actions">
        <button className="mini-button" disabled={appointment.status === 'approved'} onClick={() => onApprove(appointment.reference)}>
          Approve
        </button>{' '}
        <button className="mini-button danger" disabled={appointment.status === 'cancelled'} onClick={() => onCancel(appointment.reference)}>
          Cancel
        </button>
      </td>
    </tr>
  );
};

export default AppointmentRow;