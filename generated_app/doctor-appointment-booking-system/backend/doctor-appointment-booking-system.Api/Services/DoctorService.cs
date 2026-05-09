using DoctorAppointmentBooking.Api.Models;

namespace DoctorAppointmentBooking.Api.Services;

public class DoctorService
{
    private readonly List<Doctor> _store = new()
    {
        new Doctor
        {
            Id = 1, Name = "Dr. Smith", Specialization = "Cardiology",
            Clinic = "Heart Center", Location = "City A", Fees = 100,
            AvailableSlots = new() { new Slot { Time = "09:00 AM" }, new Slot { Time = "10:00 AM" } }
        },
        new Doctor
        {
            Id = 2, Name = "Dr. Jane", Specialization = "Dermatology",
            Clinic = "Skin Clinic", Location = "City B", Fees = 120,
            AvailableSlots = new() { new Slot { Time = "11:00 AM", IsBooked = true }, new Slot { Time = "01:00 PM" } }
        },
    };

    public IEnumerable<Doctor> Search(string? specialization, string? clinic, string? location) =>
        _store.Where(d =>
            (specialization == null || d.Specialization == specialization) &&
            (clinic == null || d.Clinic == clinic) &&
            (location == null || d.Location == location));

    public Doctor? GetById(int id) => _store.FirstOrDefault(d => d.Id == id);
}
