using DoctorAppointmentBooking.Api.Models;

namespace DoctorAppointmentBooking.Api.Services;

public class AppointmentService
{
    private readonly List<AppointmentModel> _store = new();

    public AppointmentModel Create(AppointmentModel a)
    {
        a.Id = _store.Count + 1;
        _store.Add(a);
        return a;
    }

    public IEnumerable<AppointmentModel> All() => _store;
}
