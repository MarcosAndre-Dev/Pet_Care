from pydantic import Field, BaseModel, EmailStr, field_validator
from typing import Literal
from datetime import date

class Tutores(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    telefone: str = Field(...)
    email: EmailStr

class Pets(BaseModel):
    nome: str = Field(min_length=2,max_length=60)
    especie: Literal["cachorro", "gato", "ave", "roedor", "outro"]
    raca: str = Field(min_length=1, max_length=60)
    peso_kg: float = Field(gt=0, le=200)
    data_nascimento: date
    @field_validator("data_nascimento")
    @classmethod
    def nao_ser_futuro(cls, valor):
        if valor > date.today():
            raise ValueError("A dara não pode ser futura")
        return valor
    tutor_id: int

class Login(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)

# CREATE TABLE pets (
#     id BIGSERIAL PRIMARY KEY,
#     nome VARCHAR(60) NOT NULL,
#     especie VARCHAR(20) NOT NULL,
#     raca VARCHAR(60) NULL,
#     data_nascimento DATE NOT NULL,
#     peso_kg NUMERIC(5,2) NOT NULL,
#     tutor_id BIGINT NOT NULL,
#     CONSTRAINT fk_pets_tutor FOREIGN KEY (tutor_id)
#         REFERENCES tutores (id) ON DELETE CASCADE
# );

# CREATE TABLE usuarios (
#     id BIGSERIAL PRIMARY KEY,
#     nome VARCHAR(100) NOT NULL,
#     email VARCHAR(150) NOT NULL,
#     senha_hash VARCHAR(255) NOT NULL,
#     CONSTRAINT uq_usuarios_email UNIQUE (email)
# );

# CREATE TABLE tokens (
#     id BIGSERIAL PRIMARY KEY,
#     usuario_id BIGINT NOT NULL,
#     token VARCHAR(64) NOT NULL,
#     expira_em TIMESTAMP NOT NULL,
#     CONSTRAINT uq_tokens_token UNIQUE (token),
#     CONSTRAINT fk_tokens_usuario FOREIGN KEY (usuario_id)
#         REFERENCES usuarios (id) ON DELETE CASCADE
# );
