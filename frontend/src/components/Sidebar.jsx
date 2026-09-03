import { NavLink } from "react-router-dom";

function Sidebar() {
  const links = [
    { to: "/", label: "Dashboard" },
    { to: "/produtos", label: "Produtos" },
    { to: "/clientes", label: "Clientes" },
    { to: "/importar", label: "Importar Dados" },
    { to: "/insights", label: "Insights" },
  ];

  return (
    <aside style={{ width: "220px", background: "#1e293b", height: "100vh", padding: "1.5rem 1rem" }}>
      <h2 style={{ color: "#fff", marginBottom: "2rem", fontSize: "1.25rem" }}>SalesInsight</h2>
      <nav style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            style={({ isActive }) => ({
              color: isActive ? "#fff" : "#94a3b8",
              background: isActive ? "#334155" : "transparent",
              padding: "0.6rem 0.8rem",
              borderRadius: "6px",
              textDecoration: "none",
              fontSize: "0.95rem",
            })}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;