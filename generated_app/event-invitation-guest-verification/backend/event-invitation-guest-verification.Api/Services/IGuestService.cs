using EventInvitation.Api.Models;

namespace EventInvitation.Api.Services;

public enum VerificationStatus
{
    Authorized,
    NotVerified,
    NotAuthorized
}

public class VerificationResult
{
    public VerificationStatus Status { get; set; }
    public Guest? Guest { get; set; }
}

public interface IGuestService
{
    VerificationResult Verify(string mobileNumber);
}
