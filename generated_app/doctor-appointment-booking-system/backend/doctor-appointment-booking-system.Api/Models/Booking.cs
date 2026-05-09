namespace DoctorAppointmentBooking.Api.Models;

public class Booking
{
    public string Reference { get; set; } = "";
    public int DoctorId { get; set; }
    public string PatientName { get; set; } = "";
    public string Mobile { get; set; } = "";
    public string Email { get; set; } = "";
    public int Age { get; set; }
    public string Reason { get; set; } = "";
    public string Slot { get; set; } = "";
    public DateTime AppointmentDate { get; set; }
    public string Status { get; set; } = "pending";
}
