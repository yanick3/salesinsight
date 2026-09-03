import { useState, useEffect } from "react";
import api from "../services/api";

function Insights() {
  const [insights, setInsights] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    api
      .get("/insights/")
      .then((resposta) => {
        setInsights(resposta.data.insights);
        setCarregando(false);
      })
      .catch((erro) => {
        console.error(erro);
        setErro("Não foi possível carregar os insights.");
        setCarregando(false);
      });
  }, []);

  if (carregando) return <p>Carregando insights...</p>;
  if (erro) return <p style={{ color: "red" }}>{erro}</p>;

  return (
    <div>
      <h1>Insights</h1>
      <ul style={{ marginTop: "1rem", lineHeight: "2" }}>
        {insights.map((frase, indice) => (
          <li key={indice}>{frase}</li>
        ))}
      </ul>
    </div>
  );
}

export default Insights;