using EventInvitation.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace EventInvitation.Api.Controllers;

[ApiController]
[Route("api/guests")]
public class GuestsController : ControllerBase
{
    private readonly IGuestService _service;

    public GuestsController(IGuestService service) => _service = service;

    public record VerifyRequest(string MobileNumber);

    [HttpPost("verify")]
    public IActionResult Verify([FromBody] VerifyRequest request)
    {
        if (request is null || string.IsNullOrWhiteSpace(request.MobileNumber))
        {
            return BadRequest(new { message = "mobileNumber is required" });
        }

        var result = _service.Verify(request.MobileNumber);

        return result.Status switch
        {
            VerificationStatus.Authorized   => Ok(result.Guest),
            VerificationStatus.NotVerified  => StatusCode(403, new { message = "not verified" }),
            VerificationStatus.NotAuthorized => NotFound(new { message = "not authorized" }),
            _ => StatusCode(500, new { message = "unknown verification status" })
        };
    }
}
