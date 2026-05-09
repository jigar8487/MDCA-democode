# Event invitation & guest verification (generated sample)

Agent-generated **Metronix EVENT SUITE**–style UI: guests verify with a **registered mobile number**, then view **event invitation** details and confirm attendance. Backend is **ASP.NET Core (.NET 9)** minimal API; frontend is **Vite + React 18 + TypeScript** with `/api` proxied to the API.

This folder is **demo output** from the Wanddy agent chain — not a separately audited product.

## Run locally

**Terminal 1 — API** (listens on **http://localhost:5500** per `Program.cs`):

```bash
cd generated_app/event-invitation-guest-verification/backend
dotnet run --project event-invitation-guest-verification.Api/event-invitation-guest-verification.Api.csproj
```

**Terminal 2 — UI** (Vite dev server on **http://localhost:5174**, proxies `/api` → `5500`):

```bash
cd generated_app/event-invitation-guest-verification/frontend
npm install
npm run dev
```

Open the printed URL (typically `http://localhost:5174`). Use demo hints shown on the **Verify** screen (verified vs unverified test numbers) to exercise the flow.

## Screenshots

See the root [README](../../README.md) (section **Sample UI — event invitation & guest verification**) for committed UI captures of verify → invitation → attendance confirmation.
