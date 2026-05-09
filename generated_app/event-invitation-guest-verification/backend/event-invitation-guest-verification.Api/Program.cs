using EventInvitation.Api.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

// Register services (interface-based DI)
builder.Services.AddSingleton<IEventService, EventService>();
builder.Services.AddSingleton<IGuestService, GuestService>();

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
        policy.SetIsOriginAllowed(static origin =>
                Uri.TryCreate(origin, UriKind.Absolute, out var uri)
                && (uri.Host.Equals("localhost", StringComparison.OrdinalIgnoreCase)
                    || uri.Host.Equals("127.0.0.1")))
              .AllowAnyHeader()
              .AllowAnyMethod());
});

builder.WebHost.UseUrls("http://localhost:5500");

var app = builder.Build();

app.UseCors();
app.MapControllers();
app.Run();
