from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class Tutor(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    telefone: str
    email: EmailStr


class Pet(BaseModel):
    nome: str = Field(min_length=2, max_length=60)
    especie: Literal["cachorro", "gato", "ave", "roedor", "outro"]
    raca: Optional[str] = None
    data_nascimento: date
    peso_kg: float = Field(gt=0, le=200)
    tutor_id: int

    @field_validator("data_nascimento")
    @classmethod
    def nao_pode_ser_futura(cls, valor):
        if valor > date.today():
            raise ValueError("data_nascimento não pode ser futura")
        return valor


class Login(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)