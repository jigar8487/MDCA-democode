using EventInvitation.Api.Models;

namespace EventInvitation.Api.Services;

public class EventService : IEventService
{
    private readonly List<Event> _store = new()
    {
        new Event
        {
            Id = 1,
            Title = "Annual Gala 2026",
            DateTimeUtc = new DateTime(2026, 6, 15, 18, 30, 0, DateTimeKind.Utc),
            Venue = "Taj Palace, Mumbai",
            Host = "WanBuffer Team",
            Description = "Join us for an exclusive evening of celebration, networking, and recognition. Black-tie attire requested. Dinner and entertainment included."
        },
        new Event
        {
            Id = 2,
            Title = "Tech Innovators Summit",
            DateTimeUtc = new DateTime(2026, 7, 22, 9, 0, 0, DateTimeKind.Utc),
            Venue = "Bangalore International Convention Centre",
            Host = "Innovation Council",
            Description = "A full-day summit featuring keynotes from top technology leaders, panel discussions, and hands-on workshops."
        }
    };

    public Event? GetById(int id) => _store.FirstOrDefault(e => e.Id == id);

    public IEnumerable<Event> All() => _store;
}
