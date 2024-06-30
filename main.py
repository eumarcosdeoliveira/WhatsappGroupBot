from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import sqlite3
import pywhatkit as wa
import time
import os
import pyautogui

app = FastAPI()

# Montando a pasta estática para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelo Pydantic para entrada de dados
class Group(BaseModel):
    group_id: str

class Message(BaseModel):
    message: str

# Função para obter uma nova conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('groups.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela de grupos no banco de dados se não existir
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY, group_id TEXT)''')
    conn.commit()
    conn.close()

create_tables()

# Endpoint para servir a página HTML
@app.get("/", response_class=HTMLResponse)
def get_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        with open(index_path) as f:
            return f.read()
    else:
        raise HTTPException(status_code=404, detail="Index file not found")

# Endpoint para listar todos os IDs de grupos
@app.get("/groups", response_model=List[Group])
def list_groups():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM groups")
    groups = cursor.fetchall()
    conn.close()
    return [{"group_id": group["group_id"]} for group in groups]

# Endpoint para adicionar um novo ID de grupo
@app.post("/groups")
def add_group(group: Group):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groups (group_id) VALUES (?)", (group.group_id,))
    conn.commit()
    conn.close()
    return {"status": "Group ID added successfully!"}

# Endpoint para excluir um ID de grupo
@app.delete("/groups/{group_id}")
def delete_group(group_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM groups WHERE group_id = ?", (group_id,))
    conn.commit()
    conn.close()
    return {"status": "Group ID deleted successfully!"}

# Endpoint para contar o número de grupos cadastrados
@app.get("/group_count")
def count_groups():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM groups")
    count = cursor.fetchone()["count"]
    conn.close()
    return {"count": count}

# Endpoint para enviar mensagem a um grupo específico
@app.post("/zap")
async def envia_msg(request: Request):
    data = await request.json()
    group_id = data.get("group_id")
    message = data.get("message")

    if not group_id:
        raise HTTPException(status_code=400, detail="Group ID is required")

    wa.sendwhatmsg_to_group_instantly(group_id, message, tab_close=True)
    return {"status": "Mensagem enviada com sucesso!"}

# Endpoint para enviar mensagem para todos os grupos cadastrados
@app.post("/zap_all")
async def envia_msg_todos(message: Message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM groups")
    groups = cursor.fetchall()
    conn.close()

    total_groups = len(groups)
    log = []
    progress = 0

    for idx, group in enumerate(groups):
        try:
            wa.sendwhatmsg_to_group_instantly(group["group_id"], message.message, tab_close=True)
            time.sleep(10)  # Tempo suficiente para enviar a mensagem e fechar a aba

            # Fechar a aba do navegador usando pyautogui
            # Esperar um pouco antes de enviar a próxima mensagem

            # Abrir uma nova aba para o próximo envio


            log.append(f"Mensagem enviada para o grupo {group['group_id']}")
            progress = (idx + 1) / total_groups * 100
        except Exception as e:
            log.append(f"Erro ao enviar mensagem para o grupo {group['group_id']}: {e}")

    return {"status": "Mensagens enviadas com sucesso!", "log": log, "progress": progress}
