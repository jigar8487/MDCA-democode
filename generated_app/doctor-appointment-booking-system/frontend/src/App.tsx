import React, { useState } from "react";
import SearchDoctors from "./views/pages/SearchDoctors";
import BookAppointment from "./views/pages/BookAppointment";
import AdminDashboard from "./views/pages/AdminDashboard";
import type { Doctor } from "./models/types";

type Route = "search" | "book" | "admin";

const App: React.FC = () => {
  const [route, setRoute] = useState<Route>("search");
  const [picked, setPicked] = useState<Doctor | null>(null);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">M</div>
          <div>
            <strong>Matronix</strong>
            <span>Care Suite</span>
          </div>
        </div>

        <nav className="side-nav">
          <button className={route === "search" ? "active" : ""} onClick={() => setRoute("search")}>
            <span>Search</span>
            <small>Doctors</small>
          </button>
          <button className={route === "admin" ? "active" : ""} onClick={() => setRoute("admin")}>
            <span>Admin</span>
            <small>Dashboard</small>
          </button>
        </nav>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow">Doctor Appointment Booking</p>
            <h1>Healthcare Operations Console</h1>
          </div>
          <div className="topbar-card">
            <span>Today</span>
            <strong>{new Date().toLocaleDateString()}</strong>
          </div>
        </header>

        {route === "search" && (
          <SearchDoctors
            onSelect={(d) => {
              setPicked(d);
              setRoute("book");
            }}
          />
        )}

        {route === "book" && picked && <BookAppointment doctor={picked} />}

        {route === "admin" && <AdminDashboard />}
      </main>
    </div>
  );
};

export default App;
