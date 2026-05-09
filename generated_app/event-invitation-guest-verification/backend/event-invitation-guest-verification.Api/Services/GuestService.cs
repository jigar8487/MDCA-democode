using EventInvitation.Api.Models;

namespace EventInvitation.Api.Services;

public class GuestService : IGuestService
{
    private readonly IEventService _eventService;

    private readonly List<Guest> _store = new()
    {
        new Guest { Id = 1, Name = "Aarav Sharma",  MobileNumber = "+91-9876543210", IsVerified = true,  EventId = 1 },
        new Guest { Id = 2, Name = "Priya Patel",   MobileNumber = "+91-9123456789", IsVerified = true,  EventId = 1 },
        new Guest { Id = 3, Name = "Rahul Mehta",   MobileNumber = "+91-9988776655", IsVerified = false, EventId = 1 },
        new Guest { Id = 4, Name = "Sneha Iyer",    MobileNumber = "+91-9765432109", IsVerified = true,  EventId = 2 },
        new Guest { Id = 5, Name = "Vikram Joshi",  MobileNumber = "+91-9012345678", IsVerified = true,  EventId = 2 },
        new Guest { Id = 6, Name = "Neha Kapoor",   MobileNumber = "+91-9876501234", IsVerified = false, EventId = 2 }
    };

    public GuestService(IEventService eventService)
    {
        _eventService = eventService;
    }

    public VerificationResult Verify(string mobileNumber)
    {
        var normalized = Normalize(mobileNumber);
        var guest = _store.FirstOrDefault(g => Normalize(g.MobileNumber) == normalized);

        if (guest is null)
        {
            return new VerificationResult { Status = VerificationStatus.NotAuthorized };
        }

        if (!guest.IsVerified)
        {
            return new VerificationResult { Status = VerificationStatus.NotVerified, Guest = guest };
        }

        // Attach event details to the guest
        guest.Event = _eventService.GetById(guest.EventId);
        return new VerificationResult { Status = VerificationStatus.Authorized, Guest = guest };
    }

    private static string Normalize(string number)
    {
        if (string.IsNullOrWhiteSpace(number)) return "";
        return new string(number.Where(char.IsDigit).ToArray());
    }
}
