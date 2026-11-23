import psycopg2
from fastapi import APIRouter, Depends, HTTPException

from database.database import conectar
from database.models import Tutor
from routers.auth import exigir_token

router = APIRouter()


def _linha_para_dict(linha):
    return {"id": linha[0], "nome": linha[1], "telefone": linha[2], "email": linha[3]}


def buscar_tutor_ou_404(tutor_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, telefone, email FROM tutores WHERE id = %s", (tutor_id,)
    )
    linha = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not linha:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")

    return _linha_para_dict(linha)


@router.get("/tutores")
def listar_tutores(token: str = Depends(exigir_token)):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, telefone, email FROM tutores ORDER BY id")
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    tutores = [_linha_para_dict(l) for l in linhas]
    return {"total": len(tutores), "tutores": tutores}


@router.get("/tutores/{tutor_id}")
def buscar_tutor(tutor_id: int, token: str = Depends(exigir_token)):
    return buscar_tutor_ou_404(tutor_id)


@router.get("/tutores/{tutor_id}/pets")
def listar_pets_do_tutor(tutor_id: int, token: str = Depends(exigir_token)):
    buscar_tutor_ou_404(tutor_id)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """SELECT id, nome, especie, raca, data_nascimento, peso_kg, tutor_id
           FROM pets WHERE tutor_id = %s ORDER BY id""",
        (tutor_id,),
    )
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    return [
        {
            "id": l[0], "nome": l[1], "especie": l[2], "raca": l[3],
            "data_nascimento": l[4], "peso_kg": float(l[5]), "tutor_id": l[6],
        }
        for l in linhas
    ]


@router.post("/tutores", status_code=201)
def criar_tutor(tutor: Tutor, token: str = Depends(exigir_token)):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO tutores (nome, telefone, email) VALUES (%s, %s, %s) RETURNING id",
            (tutor.nome, tutor.telefone, tutor.email),
        )
        novo_id = cursor.fetchone()[0]
        conexao.commit()
    except psycopg2.errors.UniqueViolation:
        conexao.rollback()
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    finally:
        cursor.close()
        conexao.close()

    return {"id": novo_id}


@router.put("/tutores/{tutor_id}")
def atualizar_tutor(tutor_id: int, tutor: Tutor, token: str = Depends(exigir_token)):
    buscar_tutor_ou_404(tutor_id)

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE tutores SET nome = %s, telefone = %s, email = %s WHERE id = %s",
            (tutor.nome, tutor.telefone, tutor.email, tutor_id),
        )
        conexao.commit()
    except psycopg2.errors.UniqueViolation:
        conexao.rollback()
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    finally:
        cursor.close()
        conexao.close()

    return buscar_tutor_ou_404(tutor_id)


@router.delete("/tutores/{tutor_id}", status_code=204)
def excluir_tutor(tutor_id: int, token: str = Depends(exigir_token)):
    buscar_tutor_ou_404(tutor_id)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tutores WHERE id = %s", (tutor_id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return None