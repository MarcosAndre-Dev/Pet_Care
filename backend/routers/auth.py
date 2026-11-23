import secrets
from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, Depends, Header, HTTPException

from database.database import conectar
from database.models import Login

router = APIRouter()


def exigir_token(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token não informado")

    token = authorization[7:]

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id FROM tokens WHERE token = %s AND expira_em > NOW()",
        (token,),
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not resultado:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    return token

MAX_TENTATIVAS = 5
BLOQUEIO_MINUTOS = 15

@router.post("/login", status_code=200)
def login(dados: Login):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, senha_hash, tentativas_falhas, bloqueado_ate FROM usuarios WHERE email = %s",
        (dados.email,),
    )
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conexao.close()
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

    usuario_id, senha_hash, tentativas_falhas, bloqueado_ate = usuario

    if bloqueado_ate and bloqueado_ate > datetime.now():
        cursor.close()
        conexao.close()
        raise HTTPException(
            status_code=429,
            detail=f"Muitas tentativas. Tente novamente após {bloqueado_ate.strftime('%H:%M:%S')}",
        )

    if not bcrypt.checkpw(dados.senha.encode(), senha_hash.encode()):
        tentativas_falhas += 1
        if tentativas_falhas >= MAX_TENTATIVAS:
            novo_bloqueio = datetime.now() + timedelta(minutes=BLOQUEIO_MINUTOS)
            cursor.execute(
                "UPDATE usuarios SET tentativas_falhas = 0, bloqueado_ate = %s WHERE id = %s",
                (novo_bloqueio, usuario_id),
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET tentativas_falhas = %s WHERE id = %s",
                (tentativas_falhas, usuario_id),
            )
        conexao.commit()
        cursor.close()
        conexao.close()
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

    cursor.execute(
        "UPDATE usuarios SET tentativas_falhas = 0, bloqueado_ate = NULL WHERE id = %s",
        (usuario_id,),
    )

    token = secrets.token_hex(32)
    expira_em = datetime.now() + timedelta(hours=2)

    cursor.execute(
        "INSERT INTO tokens (usuario_id, token, expira_em) VALUES (%s, %s, %s)",
        (usuario_id, token, expira_em),
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    return {"token": token, "tipo": "Bearer", "expira_em": expira_em}

@router.post("/logout", status_code=204)
def logout(token: str = Depends(exigir_token)):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tokens WHERE token = %s", (token,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return None