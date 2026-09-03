import { useState, useEffect } from "react";
import api from "../services/api";

function Clientes() {
  const [clientes, setClientes] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    api
      .get("/clientes/")
      .then((resposta) => {
        setClientes(resposta.data);
        setCarregando(false);
      })
      .catch((erro) => {
        console.error(erro);
        setErro("Não foi possível carregar os clientes.");
        setCarregando(false);
      });
  }, []);

  if (carregando) return <p>Carregando clientes...</p>;
  if (erro) return <p style={{ color: "red" }}>{erro}</p>;

  return (
    <div>
      <h1>Clientes</h1>
      <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "1rem" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "2px solid #e2e8f0" }}>
            <th style={{ padding: "0.5rem" }}>ID</th>
            <th style={{ padding: "0.5rem" }}>Nome</th>
            <th style={{ padding: "0.5rem" }}>Email</th>
          </tr>
        </thead>
        <tbody>
          {clientes.map((cliente) => (
            <tr key={cliente.id} style={{ borderBottom: "1px solid #f1f5f9" }}>
              <td style={{ padding: "0.5rem" }}>{cliente.id}</td>
              <td style={{ padding: "0.5rem" }}>{cliente.nome}</td>
              <td style={{ padding: "0.5rem" }}>{cliente.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Clientes;