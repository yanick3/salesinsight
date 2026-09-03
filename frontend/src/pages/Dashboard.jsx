import { useState, useEffect } from "react";
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";
import api from "../services/api";
import CardMetrica from "../components/CardMetrica";

const CORES = ["#3b82f6", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6"];

function formatarMoeda(valor) {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function Dashboard() {
  const [metricas, setMetricas] = useState(null);
  const [vendasPorMes, setVendasPorMes] = useState([]);
  const [produtosMaisVendidos, setProdutosMaisVendidos] = useState([]);
  const [faturamentoPorCategoria, setFaturamentoPorCategoria] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    Promise.all([
      api.get("/dashboard/"),
      api.get("/dashboard/vendas-por-mes"),
      api.get("/dashboard/produtos-mais-vendidos"),
      api.get("/dashboard/faturamento-por-categoria"),
    ])
      .then(([resMetricas, resVendasMes, resProdutos, resCategorias]) => {
        setMetricas(resMetricas.data);
        setVendasPorMes(resVendasMes.data);
        setProdutosMaisVendidos(resProdutos.data);
        setFaturamentoPorCategoria(resCategorias.data);
        setCarregando(false);
      })
      .catch((erroRequisicao) => {
        console.error(erroRequisicao);
        setErro("Não foi possível carregar o dashboard.");
        setCarregando(false);
      });
  }, []);

  if (carregando) return <p>Carregando dashboard...</p>;
  if (erro) return <p style={{ color: "red" }}>{erro}</p>;

  return (
    <div>
      <h1>Dashboard</h1>

      <div style={{ display: "flex", gap: "1rem", marginTop: "1.5rem" }}>
        <CardMetrica titulo="Faturamento Total" valor={formatarMoeda(metricas.faturamento_total)} />
        <CardMetrica titulo="Quantidade de Vendas" valor={metricas.quantidade_vendas} />
        <CardMetrica titulo="Ticket Médio" valor={formatarMoeda(metricas.ticket_medio)} />
        <CardMetrica titulo="Produto Mais Vendido" valor={metricas.produto_mais_vendido || "-"} />
        <CardMetrica titulo="Melhor Cliente" valor={metricas.cliente_que_mais_comprou || "-"} />
      </div>

      <div style={{ display: "flex", gap: "1.5rem", marginTop: "2rem", flexWrap: "wrap" }}>
        <div style={{ background: "#fff", borderRadius: "8px", padding: "1rem", flex: "1 1 400px" }}>
          <h3 style={{ marginBottom: "1rem" }}>Evolução das Vendas (Faturamento por Mês)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={vendasPorMes}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mes" />
              <YAxis />
              <Tooltip formatter={(valor) => formatarMoeda(valor)} />
              <Line type="monotone" dataKey="faturamento" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ background: "#fff", borderRadius: "8px", padding: "1rem", flex: "1 1 400px" }}>
          <h3 style={{ marginBottom: "1rem" }}>Produtos Mais Vendidos</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={produtosMaisVendidos}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="produto" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="quantidade_vendida" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={{ background: "#fff", borderRadius: "8px", padding: "1rem", flex: "1 1 400px" }}>
          <h3 style={{ marginBottom: "1rem" }}>Faturamento por Categoria</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={faturamentoPorCategoria}
                dataKey="faturamento"
                nameKey="categoria"
                cx="50%"
                cy="50%"
                outerRadius={90}
                label
              >
                {faturamentoPorCategoria.map((_, indice) => (
                  <Cell key={indice} fill={CORES[indice % CORES.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(valor) => formatarMoeda(valor)} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;