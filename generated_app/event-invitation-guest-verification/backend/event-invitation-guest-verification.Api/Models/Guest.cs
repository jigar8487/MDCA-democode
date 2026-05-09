namespace EventInvitation.Api.Models;

public class Guest
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string MobileNumber { get; set; } = "";
    public bool IsVerified { get; set; }
    public int EventId { get; set; }
    public Event? Event { get; set; }
}
