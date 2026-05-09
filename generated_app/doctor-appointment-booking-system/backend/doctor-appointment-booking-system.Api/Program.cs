var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSingleton<DoctorAppointmentBooking.Api.Services.DoctorService>();
builder.Services.AddSingleton<DoctorAppointmentBooking.Api.Services.BookingService>();
builder.Services.AddSingleton<DoctorAppointmentBooking.Api.Services.AppointmentService>();
builder.Services.AddCors(o => o.AddDefaultPolicy(p => p.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()));

var app = builder.Build();
app.UseCors();
app.MapControllers();
app.Run();
