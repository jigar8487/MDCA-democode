export interface Doctor {
  id: number;
  name: string;
  specialization: string;
  clinic: string;
  location: string;
  fees: number;
  availableSlots: Slot[];
}

export interface Slot {
  time: string;
  isBooked: boolean;
}

export interface Booking {
  reference: string;
  doctorId: number;
  patientName: string;
  mobile: string;
  email: string;
  age: number;
  reason: string;
  slot: string;
  appointmentDate: string;
  status: string;
}