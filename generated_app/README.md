# generated_app

The orchestrator’s developer agent writes new apps here (`generated_app/<slug>/`).

**What is in git:** One **sample** scaffold — [`doctor-appointment-booking-system/`](doctor-appointment-booking-system/) — so clones include an example of agent-generated .NET 9 + React 18 code. It was produced by the multi-agent flow (not hand-maintained as a product).

**What stays local:** Any other slugs you generate are **gitignored** so accidental noise (`node_modules`, other experiments) is not published. After `npm install` / `dotnet build`, build artifacts under this tree remain ignored when applicable.

To run the sample, see `doctor-appointment-booking-system/frontend/README.md` and the backend `.csproj` under `backend/`.
