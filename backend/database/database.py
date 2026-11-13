import os
import psycopg2
from dotenv import load_dotenv

def conectar():
    return psycopg2.connect(
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("SENHA")
    )
conexao = conectar()
tutores=conexao.tutores()
tutores.execute("SELECT nome FROM tutores WHERE id = %s", (1,))
resultado = tutores.fetchone()
print(resultado)
tutores.close()
conexao.close()