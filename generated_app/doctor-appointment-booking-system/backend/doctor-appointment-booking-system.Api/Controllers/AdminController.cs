using DoctorAppointmentBooking.Api.Models;
using DoctorAppointmentBooking.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DoctorAppointmentBooking.Api.Controllers;

[ApiController]
[Route("api/admin")]
public class AdminController : ControllerBase
{
    private readonly BookingService _bookings;
    public AdminController(BookingService bookings) => _bookings = bookings;

    [HttpGet("appointments")]
    public ActionResult<IEnumerable<Booking>> List([FromQuery] string? status = null)
    {
        var all = _bookings.All();
        return Ok(status is null ? all : all.Where(b => b.Status == status));
    }

    [HttpPost("appointments/{bookingRef}/approve")]
    public IActionResult Approve(string bookingRef)
    {
        var b = _bookings.Get(bookingRef);
        if (b is null) return NotFound();
        b.Status = "approved";
        return NoContent();
    }

    [HttpPost("appointments/{bookingRef}/cancel")]
    public IActionResult Cancel(string bookingRef) =>
        _bookings.Cancel(bookingRef) ? NoContent() : NotFound();

    [HttpGet("reports/daily")]
    public ActionResult<object> Daily()
    {
        var today = DateTime.UtcNow.Date;
        var todays = _bookings.All().Where(b => b.AppointmentDate.Date == today).ToList();
        return Ok(new { date = today, total = todays.Count, items = todays });
    }

    [HttpGet("reports/monthly")]
    public ActionResult<object> Monthly()
    {
        var now = DateTime.UtcNow;
        var monthly = _bookings.All().Where(b => b.AppointmentDate.Year == now.Year && b.AppointmentDate.Month == now.Month).ToList();
        return Ok(new { year = now.Year, month = now.Month, total = monthly.Count });
    }
}
