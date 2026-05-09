using DoctorAppointmentBooking.Api.Models;
using DoctorAppointmentBooking.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DoctorAppointmentBooking.Api.Controllers;

[ApiController]
[Route("api/doctors")]
public class DoctorController : ControllerBase
{
    private readonly DoctorService _service;
    public DoctorController(DoctorService service) => _service = service;

    [HttpGet]
    public ActionResult<IEnumerable<Doctor>> Search(
        [FromQuery] string? specialization, [FromQuery] string? clinic, [FromQuery] string? location)
        => Ok(_service.Search(specialization, clinic, location));

    [HttpGet("{id:int}")]
    public ActionResult<Doctor> GetById(int id)
    {
        var doctor = _service.GetById(id);
        return doctor is null ? NotFound() : Ok(doctor);
    }
}
