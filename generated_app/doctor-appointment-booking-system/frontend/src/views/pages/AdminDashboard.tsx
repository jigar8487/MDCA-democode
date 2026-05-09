import React, { useEffect } from 'react';
import { useAdmin } from '../../controllers/useAdmin';
import AppointmentRow from '../components/AppointmentRow';

const AdminDashboard: React.FC = () => {
  const { appointments, fetchAppointments, updateAppointmentStatus, isLoading, error } = useAdmin();

  useEffect(() => {
    fetchAppointments();
  }, [fetchAppointments]);

  return (
    <section className="page-section">
      <div className="section-header">
        <div>
          <p className="eyebrow">Operations</p>
          <h2>Admin Dashboard</h2>
          <p className="muted">Review appointment requests and manage booking status.</p>
        </div>
        <button className="secondary-button" onClick={fetchAppointments}>Refresh Appointments</button>
      </div>

      {isLoading && <p className="state-card">Loading appointments...</p>}
      {error && <p className="state-card error">{error}</p>}
      {!isLoading && !error && appointments.length === 0 && (
        <p className="state-card">No appointments found. Book an appointment first, then refresh this dashboard.</p>
      )}

      {appointments.length > 0 && (
        <div className="table-card">
          <table>
            <thead>
              <tr>
                <th>Reference</th>
                <th>Patient</th>
                <th>Mobile</th>
                <th>Email</th>
                <th>Slot</th>
                <th>Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map(appointment => (
                <AppointmentRow
                  key={appointment.reference}
                  appointment={appointment}
                  onApprove={bookingRef => updateAppointmentStatus(bookingRef, 'approve')}
                  onCancel={bookingRef => updateAppointmentStatus(bookingRef, 'cancel')}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
};

export default AdminDashboard;