# PetCare — API REST em Python 

Mesmo tema do Trabalho 1 (clínica veterinária PetCare), agora implementado em **Python com FastAPI** e banco **PostgreSQL**.

## 📋 Sobre o projeto

API para gerenciar os tutores (donos) e os pets de uma clínica veterinária:

- Todas as rotas exigem autenticação por token, exceto `POST /login`.
- Funcionários autenticados podem consultar, cadastrar, alterar e excluir tutores e pets.

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
│ ├── auth.py # login/logout e verificação de token
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

pip install fastapi uvicorn psycopg2-binary python-dotenv email-validator bcrypt

uvicorn main:app --reload
```

A API fica disponível em `http://localhost:8000`.

### Banco de dados

1. Crie o banco `petcare` no PostgreSQL.
2. Execute o script de criação das tabelas (`banco.sql`, na raiz do projeto).
3. Crie um arquivo `.env` dentro de `backend/` com: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.

### Frontend

Abra os arquivos da pasta `frontend/html/` com uma extensão como *Live Server* (não funciona abrindo o arquivo direto, por causa do CORS).

## 🔑 Autenticação e segurança

- `POST /login` devolve um token válido por 2 horas.
- Todas as demais rotas exigem o cabeçalho `Authorization: Bearer <token>`.
- `POST /logout` invalida o token.
- CORS restrito à origem do frontend.
- Limite de tentativas de login para evitar força bruta.
- Tratamento de erros padronizado (não expõe detalhes internos do sistema).

## 👤 Usuário de teste

- **E-mail:** professor@petcare.com
- **Senha:** professor123

## 📌 Status

✅ CRUD completo de tutores e pets · ✅ autenticação por token · 🚧 reforço de segurança em andamento (CORS, limite de login, tratamento de erros).

## 👥 Integrantes

- Marcos André Camargo Belo
- Arthur Santana Rufino