namespace DoctorAppointmentBooking.Api.Models;

public class AppointmentModel
{
    public int Id { get; set; }
    public string PatientName { get; set; } = "";
    public string MobileNumber { get; set; } = "";
    public string Email { get; set; } = "";
    public int Age { get; set; }
    public string Reason { get; set; } = "";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public string Status { get; set; } = "pending";
}
