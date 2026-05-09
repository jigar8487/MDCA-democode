import React, { FormEvent, useMemo, useState } from 'react';
import { Booking, Doctor } from '../../models/types';

const API_BASE_URL = 'http://localhost:5000';

const BookAppointment: React.FC<{ doctor: Doctor }> = ({ doctor }) => {
  const availableSlots = useMemo(
    () => doctor.availableSlots.filter(slot => !slot.isBooked),
    [doctor.availableSlots]
  );
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [booking, setBooking] = useState<Booking | null>(null);
  const [form, setForm] = useState({
    patientName: '',
    mobile: '',
    email: '',
    age: '',
    reason: '',
    slot: availableSlots[0]?.time ?? '',
    appointmentDate: new Date().toISOString().slice(0, 10),
  });

  const handleBooking = () => {
    setIsFormOpen(true);
    setBooking(null);
    setError(null);
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/bookings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          doctorId: doctor.id,
          patientName: form.patientName,
          mobile: form.mobile,
          email: form.email,
          age: Number(form.age),
          reason: form.reason,
          slot: form.slot,
          appointmentDate: form.appointmentDate,
        }),
      });

      if (!response.ok) {
        throw new Error(`Booking failed (${response.status})`);
      }

      const created = await response.json();
      setBooking(created);
      setIsFormOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Booking failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="page-section">
      <div className="booking-layout">
        <div className="content-card doctor-profile">
          <span className="status-pill">Selected Doctor</span>
          <h2>Book Appointment with {doctor.name}</h2>
          <p className="muted">{doctor.specialization} at {doctor.clinic}, {doctor.location}</p>
          <div className="profile-stats">
            <div>
              <span>Consultation Fee</span>
              <strong>${doctor.fees}</strong>
            </div>
            <div>
              <span>Open Slots</span>
              <strong>{availableSlots.length}</strong>
            </div>
          </div>
          <button className="primary-button wide" onClick={handleBooking}>Book Now</button>
        </div>

        <div className="content-card">
          <h3>Patient Details</h3>
          {!isFormOpen && !booking && <p className="muted">Click Book Now to enter patient details and confirm the appointment.</p>}
          {isFormOpen && (
            <form className="form-grid" onSubmit={handleSubmit}>
              <input
                required
                placeholder="Patient name"
                value={form.patientName}
                onChange={event => setForm({ ...form, patientName: event.target.value })}
              />
              <input
                required
                placeholder="Mobile"
                value={form.mobile}
                onChange={event => setForm({ ...form, mobile: event.target.value })}
              />
              <input
                required
                type="email"
                placeholder="Email"
                value={form.email}
                onChange={event => setForm({ ...form, email: event.target.value })}
              />
              <input
                required
                min="1"
                type="number"
                placeholder="Age"
                value={form.age}
                onChange={event => setForm({ ...form, age: event.target.value })}
              />
              <textarea
                required
                placeholder="Reason for visit"
                value={form.reason}
                onChange={event => setForm({ ...form, reason: event.target.value })}
              />
              <select
                required
                value={form.slot}
                onChange={event => setForm({ ...form, slot: event.target.value })}
              >
                {availableSlots.map(slot => (
                  <option key={slot.time} value={slot.time}>{slot.time}</option>
                ))}
              </select>
              <input
                required
                type="date"
                value={form.appointmentDate}
                onChange={event => setForm({ ...form, appointmentDate: event.target.value })}
              />
              <button className="primary-button" disabled={isSubmitting || availableSlots.length === 0} type="submit">
                {isSubmitting ? 'Booking...' : 'Confirm Booking'}
              </button>
            </form>
          )}

          {error && <p className="state-card error">{error}</p>}
          {booking && (
            <p className="state-card success">
              Appointment booked. Reference: <strong>{booking.reference}</strong>
            </p>
          )}
        </div>
      </div>
    </section>
  );
};

export default BookAppointment;