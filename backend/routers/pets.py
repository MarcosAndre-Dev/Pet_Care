from typing import Optional

import psycopg2
from fastapi import APIRouter, Depends, HTTPException, Query

from database.database import conectar
from database.models import Pet
from routers.auth import exigir_token

router = APIRouter()


def _linha_para_dict(l):
    return {
        "id": l[0], "nome": l[1], "especie": l[2], "raca": l[3],
        "data_nascimento": l[4], "peso_kg": float(l[5]), "tutor_id": l[6],
    }


def buscar_pet_ou_404(pet_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """SELECT id, nome, especie, raca, data_nascimento, peso_kg, tutor_id
           FROM pets WHERE id = %s""",
        (pet_id,),
    )
    linha = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not linha:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    return _linha_para_dict(linha)


@router.get("/pets")
def listar_pets(especie: Optional[str] = Query(None), token: str = Depends(exigir_token)):
    conexao = conectar()
    cursor = conexao.cursor()

    if especie:
        cursor.execute(
            """SELECT id, nome, especie, raca, data_nascimento, peso_kg, tutor_id
               FROM pets WHERE especie = %s ORDER BY id""",
            (especie,),
        )
    else:
        cursor.execute(
            """SELECT id, nome, especie, raca, data_nascimento, peso_kg, tutor_id
               FROM pets ORDER BY id"""
        )

    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    pets = [_linha_para_dict(l) for l in linhas]
    return {"total": len(pets), "pets": pets}


@router.get("/pets/{pet_id}")
def buscar_pet(pet_id: int, token: str = Depends(exigir_token)):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """SELECT p.id, p.nome, p.especie, p.raca, p.data_nascimento, p.peso_kg,
                  p.tutor_id, t.nome
           FROM pets p JOIN tutores t ON t.id = p.tutor_id
           WHERE p.id = %s""",
        (pet_id,),
    )
    linha = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not linha:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    dados = _linha_para_dict(linha)
    dados["tutor_nome"] = linha[7]
    return dados


@router.post("/pets", status_code=201)
def criar_pet(pet: Pet, token: str = Depends(exigir_token)):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """INSERT INTO pets (nome, especie, raca, data_nascimento, peso_kg, tutor_id)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
            (pet.nome, pet.especie, pet.raca, pet.data_nascimento, pet.peso_kg, pet.tutor_id),
        )
        novo_id = cursor.fetchone()[0]
        conexao.commit()
    except psycopg2.errors.ForeignKeyViolation:
        conexao.rollback()
        raise HTTPException(status_code=422, detail="tutor_id não corresponde a um tutor existente")
    finally:
        cursor.close()
        conexao.close()

    return {"id": novo_id}


@router.put("/pets/{pet_id}")
def atualizar_pet(pet_id: int, pet: Pet, token: str = Depends(exigir_token)):
    buscar_pet_ou_404(pet_id)

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """UPDATE pets SET nome = %s, especie = %s, raca = %s,
                               data_nascimento = %s, peso_kg = %s, tutor_id = %s
               WHERE id = %s""",
            (pet.nome, pet.especie, pet.raca, pet.data_nascimento, pet.peso_kg, pet.tutor_id, pet_id),
        )
        conexao.commit()
    except psycopg2.errors.ForeignKeyViolation:
        conexao.rollback()
        raise HTTPException(status_code=422, detail="tutor_id não corresponde a um tutor existente")
    finally:
        cursor.close()
        conexao.close()

    return buscar_pet_ou_404(pet_id)


@router.delete("/pets/{pet_id}", status_code=204)
def excluir_pet(pet_id: int, token: str = Depends(exigir_token)):
    buscar_pet_ou_404(pet_id)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return None