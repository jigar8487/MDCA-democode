using EventInvitation.Api.Models;

namespace EventInvitation.Api.Services;

public interface IEventService
{
    Event? GetById(int id);
    IEnumerable<Event> All();
}
