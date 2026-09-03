function CardMetrica({ titulo, valor }) {
  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "8px",
        padding: "1.25rem",
        boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
        flex: 1,
      }}
    >
      <p style={{ color: "#64748b", fontSize: "0.85rem", marginBottom: "0.5rem" }}>{titulo}</p>
      <p style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#1e293b" }}>{valor}</p>
    </div>
  );
}

export default CardMetrica;