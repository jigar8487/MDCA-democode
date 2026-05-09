using DoctorAppointmentBooking.Api.Models;
using DoctorAppointmentBooking.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DoctorAppointmentBooking.Api.Controllers;

[ApiController]
[Route("api/bookings")]
public class BookingController : ControllerBase
{
    private readonly BookingService _service;
    public BookingController(BookingService service) => _service = service;

    [HttpPost]
    public ActionResult<Booking> Create([FromBody] Booking booking)
    {
        var created = _service.Create(booking);
        return CreatedAtAction(nameof(GetByRef), new { bookingRef = created.Reference }, created);
    }

    [HttpGet("{bookingRef}")]
    public ActionResult<Booking> GetByRef(string bookingRef)
    {
        var booking = _service.Get(bookingRef);
        return booking is null ? NotFound() : Ok(booking);
    }

    public record RescheduleDto(string Slot, DateTime AppointmentDate);

    [HttpPatch("{bookingRef}/reschedule")]
    public IActionResult Reschedule(string bookingRef, [FromBody] RescheduleDto dto) =>
        _service.Reschedule(bookingRef, dto.Slot, dto.AppointmentDate) ? NoContent() : NotFound();

    [HttpDelete("{bookingRef}")]
    public IActionResult Cancel(string bookingRef, [FromQuery] string? otp = null)
    {
        // OTP stub: accept any 6-digit otp; real impl would verify against issued code
        if (otp is null || otp.Length != 6) return BadRequest("OTP required (6 digits)");
        return _service.Cancel(bookingRef) ? NoContent() : NotFound();
    }
}
