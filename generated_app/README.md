# generated_app

The orchestrator’s developer agent writes new apps here (`generated_app/<slug>/`).

**What is in git:** Two **sample** scaffolds produced by the agent flow (not hand-maintained products):

| Sample | Stack | Purpose |
|--------|--------|---------|
| [`doctor-appointment-booking-system/`](doctor-appointment-booking-system/) | .NET 9 API + Vite React 18 | Doctor search / booking illustration |
| [`event-invitation-guest-verification/`](event-invitation-guest-verification/) | .NET 9 API + Vite React 18 | Guest mobile verify → invitation → attendance (**UI review** screenshots in root [README](../README.md)) |

**What stays local:** Any other slugs you generate are **gitignored** so accidental noise (`node_modules`, one-off experiments) is not published.

**Run:** See each sample’s `README.md` (doctor: `frontend/` + `backend/`; event invitation: same layout).
