from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = FastAPI()

# Função que lê e armazena mensagens
def ler_e_armazenar_mensagens(grupo: str):
    # Lógica para ler mensagens do grupo do WhatsApp
    mensagens = []  # Substituir com a lógica de leitura real do WhatsApp

    # Armazenar mensagens em um arquivo de texto
    arquivo_saida = f"{grupo}_mensagens.txt"
    with open(arquivo_saida, "a", encoding="utf-8") as file:
        for mensagem in mensagens:
            file.write(f"{mensagem}\n")

@app.get("/ler_mensagens/{grupo}")
def ler_mensagens(grupo: str):
    # Inicia o agendador para ler mensagens a cada 30 segundos
    scheduler.add_job(ler_e_armazenar_mensagens, 'interval', seconds=1, args=[grupo])
    return {"mensagem": "Leitura de mensagens agendada a cada 30 segundos."}

if __name__ == "__main__":
    import uvicorn
    from threading import Event

    scheduler = BackgroundScheduler()
    scheduler.start()

    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    finally:
        scheduler.shutdown()
