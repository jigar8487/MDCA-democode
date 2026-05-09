using DoctorAppointmentBooking.Api.Models;

namespace DoctorAppointmentBooking.Api.Services;

public class BookingService
{
    private readonly Dictionary<string, Booking> _bookings = new();

    public Booking Create(Booking booking)
    {
        booking.Reference = Guid.NewGuid().ToString("n").Substring(0, 8);
        booking.Status = "pending";
        _bookings[booking.Reference] = booking;
        return booking;
    }

    public Booking? Get(string bookingRef) =>
        _bookings.TryGetValue(bookingRef, out var b) ? b : null;

    public bool Reschedule(string bookingRef, string newSlot, DateTime newDate)
    {
        if (!_bookings.TryGetValue(bookingRef, out var b)) return false;
        b.Slot = newSlot;
        b.AppointmentDate = newDate;
        return true;
    }

    public bool Cancel(string bookingRef)
    {
        if (!_bookings.TryGetValue(bookingRef, out var b)) return false;
        b.Status = "cancelled";
        return true;
    }

    public IEnumerable<Booking> All() => _bookings.Values;
}
