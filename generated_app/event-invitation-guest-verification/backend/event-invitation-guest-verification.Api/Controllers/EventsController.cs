using EventInvitation.Api.Models;
using EventInvitation.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace EventInvitation.Api.Controllers;

[ApiController]
[Route("api/events")]
public class EventsController : ControllerBase
{
    private readonly IEventService _service;

    public EventsController(IEventService service) => _service = service;

    [HttpGet]
    public ActionResult<IEnumerable<Event>> GetAll() => Ok(_service.All());

    [HttpGet("{id:int}")]
    public ActionResult<Event> GetById(int id)
    {
        var ev = _service.GetById(id);
        return ev is null ? NotFound(new { message = "event not found" }) : Ok(ev);
    }
}
