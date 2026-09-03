import { useState, useEffect } from "react";
import api from "../services/api";

function Produtos() {
  const [produtos, setProdutos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    api
      .get("/produtos/")
      .then((resposta) => {
        setProdutos(resposta.data);
        setCarregando(false);
      })
      .catch((erro) => {
        console.error(erro);
        setErro("Não foi possível carregar os produtos.");
        setCarregando(false);
      });
  }, []);

  if (carregando) return <p>Carregando produtos...</p>;
  if (erro) return <p style={{ color: "red" }}>{erro}</p>;

  return (
    <div>
      <h1>Produtos</h1>
      <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "1rem" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "2px solid #e2e8f0" }}>
            <th style={{ padding: "0.5rem" }}>ID</th>
            <th style={{ padding: "0.5rem" }}>Nome</th>
            <th style={{ padding: "0.5rem" }}>Categoria ID</th>
          </tr>
        </thead>
        <tbody>
          {produtos.map((produto) => (
            <tr key={produto.id} style={{ borderBottom: "1px solid #f1f5f9" }}>
              <td style={{ padding: "0.5rem" }}>{produto.id}</td>
              <td style={{ padding: "0.5rem" }}>{produto.nome}</td>
              <td style={{ padding: "0.5rem" }}>{produto.categoria_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Produtos;