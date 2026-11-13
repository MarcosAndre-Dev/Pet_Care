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