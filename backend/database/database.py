import os
import psycopg2
from dotenv import load_dotenv

def conectar():
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
conexao = conectar()
tutores=conexao.cursor()
tutores.execute("SELECT nome FROM tutores WHERE id = %s", (1,))
resultado = tutores.fetchone()
print(resultado)
tutores.close()
conexao.close()