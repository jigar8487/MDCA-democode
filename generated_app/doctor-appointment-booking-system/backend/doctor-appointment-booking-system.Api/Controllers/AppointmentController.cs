using DoctorAppointmentBooking.Api.Models;
using DoctorAppointmentBooking.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DoctorAppointmentBooking.Api.Controllers;

[ApiController]
[Route("api/appointments")]
public class AppointmentController : ControllerBase
{
    private readonly AppointmentService _service;
    public AppointmentController(AppointmentService service) => _service = service;

    [HttpPost]
    public ActionResult<AppointmentModel> Book([FromBody] AppointmentModel appointment) =>
        Ok(_service.Create(appointment));

    [HttpGet]
    public ActionResult<IEnumerable<AppointmentModel>> All() => Ok(_service.All());
}
