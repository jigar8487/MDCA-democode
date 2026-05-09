namespace EventInvitation.Api.Models;

public class Event
{
    public int Id { get; set; }
    public string Title { get; set; } = "";
    public DateTime DateTimeUtc { get; set; }
    public string Venue { get; set; } = "";
    public string Description { get; set; } = "";
    public string Host { get; set; } = "";
}
