namespace DoctorAppointmentBooking.Api.Models;

public class Doctor
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Specialization { get; set; } = "";
    public string Clinic { get; set; } = "";
    public string Location { get; set; } = "";
    public List<Slot> AvailableSlots { get; set; } = new();
    public decimal Fees { get; set; }
}

public class Slot
{
    public string Time { get; set; } = "";
    public bool IsBooked { get; set; }
}
