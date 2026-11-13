# PetCare — API REST em Python (Trabalho 2)

Mesmo tema do Trabalho 1 (clínica veterinária PetCare), agora implementado em **Python com FastAPI** e banco **PostgreSQL**.

## 📋 Sobre o projeto

API para gerenciar os tutores (donos) e os pets de uma clínica veterinária:

- Qualquer pessoa pode **consultar** tutores e pets.
- Apenas funcionários **autenticados por token** podem cadastrar, alterar e excluir.

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3 + FastAPI + Uvicorn |
| Banco de dados | PostgreSQL (acesso via `psycopg2`, SQL puro com prepared statements) |
| Autenticação | Token aleatório com expiração (mesmo esquema do Trabalho 1 em PHP) |
| Frontend | HTML, CSS e JavaScript puro |

## 📁 Estrutura do projeto

Pet_Care/
├── backend/
│ ├── main.py # ponto de entrada da aplicação FastAPI
│ ├── database/
│ │ ├── database.py # conexão com o PostgreSQL
│ │ └── models.py # modelos/esquemas de dados
│ └── routers/
│ ├── tutores.py # rotas de tutores
│ └── pets.py # rotas de pets
├── frontend/
│ ├── html/
│ ├── css/
│ └── js/
└── README.md


## 🚀 Como rodar o projeto

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install fastapi uvicorn psycopg2-binary

uvicorn main:app --reload
```

A API fica disponível em `http://localhost:8000`.

### Banco de dados

1. Crie o banco `petcare` no PostgreSQL.
2. Execute o script de criação das tabelas (em `backend/database/`).

### Frontend

Abra os arquivos da pasta `frontend/html/` diretamente no navegador, ou sirva com uma extensão como *Live Server*.

## 🔑 Autenticação

- `POST /login` devolve um token válido por 2 horas.
- Rotas protegidas exigem o cabeçalho `Authorization: Bearer <token>`.
- `POST /logout` invalida o token.

## 👤 Usuário de teste

- **E-mail:** professor@petcare.com
- **Senha:** professor123

## 📌 Status

🚧 Projeto em desenvolvimento — próximas etapas: conexão com o banco, rotas de tutores e pets, frontend.

## 👥 Integrantes

- Marcos André Camargo Belo
- Arthur Santana Rufino