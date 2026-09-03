import { useState } from "react";
import api from "../services/api";

function Importar() {
  const [arquivo, setArquivo] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [erro, setErro] = useState(null);

  function handleSelecionarArquivo(evento) {
    setArquivo(evento.target.files[0]);
    setResultado(null);
    setErro(null);
  }

  function handleEnviar() {
    if (!arquivo) {
      setErro("Selecione um arquivo CSV antes de enviar.");
      return;
    }

    const formData = new FormData();
    formData.append("arquivo", arquivo);

    setEnviando(true);
    setErro(null);

    api
      .post("/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((resposta) => {
        setResultado(resposta.data);
        setEnviando(false);
      })
      .catch((erroRequisicao) => {
        console.error(erroRequisicao);
        const mensagem =
          erroRequisicao.response?.data?.detail || "Não foi possível importar o arquivo.";
        setErro(mensagem);
        setEnviando(false);
      });
  }

  return (
    <div>
      <h1>Importar Dados</h1>
      <p>Selecione um arquivo CSV com os dados de vendas.</p>

      <input type="file" accept=".csv" onChange={handleSelecionarArquivo} style={{ marginTop: "1rem" }} />

      <div style={{ marginTop: "1rem" }}>
        <button onClick={handleEnviar} disabled={enviando}>
          {enviando ? "Enviando..." : "Enviar arquivo"}
        </button>
      </div>

      {resultado && (
        <p style={{ color: "green", marginTop: "1rem" }}>
          {resultado.vendas_importadas} vendas importadas com sucesso!
        </p>
      )}

      {erro && <p style={{ color: "red", marginTop: "1rem" }}>{erro}</p>}
    </div>
  );
}

export default Importar;