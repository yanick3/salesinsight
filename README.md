# SalesInsight

Plataforma inteligente de análise de vendas. Permite importar dados de vendas via CSV e visualizar métricas, gráficos e insights automáticos sobre o desempenho do negócio.

Acesse o projeto: https://salesinsight-eight.vercel.app

Observação: o backend está hospedado no plano gratuito do Render, que "dorme" após períodos de inatividade. A primeira requisição após um tempo parado pode levar de 30 a 50 segundos para responder.

---

## Visão geral

O SalesInsight permite que uma empresa importe seus dados de vendas e obtenha, automaticamente:

- Dashboard com métricas principais (faturamento, ticket médio, produto mais vendido, etc.)
- Gráficos de evolução de vendas, produtos mais vendidos e faturamento por categoria
- Listagem de produtos e clientes
- Insights automáticos gerados por regras de negócio (sem uso de IA generativa)

---

## Tecnologias utilizadas

**Backend**
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pandas
- Pytest (testes automatizados)

**Frontend**
- React
- Vite
- Recharts (gráficos)
- Axios

**Infraestrutura**
- Banco de dados: Neon (PostgreSQL serverless)
- Backend: Render
- Frontend: Vercel

---

## Estrutura do projeto

```
salesinsight/
├── backend/
│   ├── app/
│   │   ├── main.py          # ponto de entrada da API
│   │   ├── database.py      # configuração do banco (SQLAlchemy)
│   │   ├── models/          # modelos das tabelas (Categoria, Produto, Cliente, Venda)
│   │   ├── schemas/         # schemas Pydantic (validação de entrada/saída)
│   │   ├── routes/          # endpoints da API
│   │   └── services/        # lógica de negócio (importação de CSV, análises com Pandas)
│   ├── tests/                # testes automatizados (pytest)
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/            # páginas (Dashboard, Produtos, Clientes, Importar, Insights)
│       ├── components/       # componentes reutilizáveis (Sidebar, CardMetrica)
│       └── services/         # configuração de chamadas à API
└── data/
    └── vendas_exemplo.csv    # arquivo de exemplo para testes
```

---

## Endpoints da API

| Método | Rota                                 | Descrição                                  |
|--------|---------------------------------------|---------------------------------------------|
| GET    | `/produtos/`                          | Lista todos os produtos                     |
| GET    | `/clientes/`                          | Lista todos os clientes                     |
| GET    | `/dashboard/`                         | Métricas principais (faturamento, ticket médio, etc.) |
| GET    | `/dashboard/vendas-por-mes`           | Faturamento agrupado por mês                |
| GET    | `/dashboard/produtos-mais-vendidos`   | Top produtos por quantidade vendida         |
| GET    | `/dashboard/faturamento-por-categoria`| Faturamento agrupado por categoria          |
| GET    | `/insights/`                          | Insights automáticos gerados por regras     |
| POST   | `/upload/`                            | Importa um arquivo CSV de vendas            |

Documentação interativa completa disponível em `/docs` (Swagger UI) na URL do backend.

---

## Rodando o projeto localmente

### Pré-requisitos
- Python 3.12+
- Node.js 18+
- PostgreSQL (local ou uma connection string de um serviço como o Neon)

### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

Crie um arquivo `.env` dentro de `backend/` com:
```
DATABASE_URL=postgresql