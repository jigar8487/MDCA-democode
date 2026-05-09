import React, { useEffect } from 'react';
import DoctorCard from '../components/DoctorCard';
import { Doctor } from '../../models/types';
import useDoctors from '../../controllers/useDoctors';

const SearchDoctors: React.FC<{ onSelect: (doctor: Doctor) => void }> = ({ onSelect }) => {
  const { doctors, fetchDoctors, isLoading, error } = useDoctors();

  useEffect(() => {
    fetchDoctors();
  }, [fetchDoctors]);

  return (
    <section className="page-section">
      <div className="section-header">
        <div>
          <p className="eyebrow">Find Care</p>
          <h2>Search Doctors</h2>
          <p className="muted">Choose a specialist and continue to appointment booking.</p>
        </div>
        <div className="metric-card">
          <span>Available Doctors</span>
          <strong>{doctors.length}</strong>
        </div>
      </div>

      {isLoading && <p className="state-card">Loading doctors...</p>}
      {error && <p className="state-card error">{error}</p>}
      {!isLoading && !error && doctors.length === 0 && <p className="state-card">No doctors found.</p>}

      <div className="doctor-grid">
        {doctors.map(doctor => <DoctorCard key={doctor.id} doctor={doctor} onSelect={onSelect} />)}
      </div>
    </section>
  );
};

export default SearchDoctors;