<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse # <-- NOVO
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(title="Sistema de Monitoramento de Fadiga - Polícia")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlertaFadiga(BaseModel):
    veiculo_id: str
    motorista_nome: str
    nivel_fadiga: str  
    ear_valor: float   
    bocejos: int       

alertas_ativos = {}

# --- [NOVA ROTA] Serve a Dashboard Web para a Polícia ---
# --- [ATUALIZADO] Serve a Dashboard Web usando caminhos absolutos ---
@app.get("/", response_class=HTMLResponse)
async def obter_dashboard():
    # Descobre a pasta onde o server.py está guardado
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    # Junta com a pasta templates e o ficheiro html
    caminho_html = os.path.join(diretorio_atual, "template", "dashboard.html")
    
    with open(caminho_html, "r", encoding="utf-8") as ficheiro:
        return ficheiro.read()

@app.post("/api/alerta")
async def receber_alerta(alerta: AlertaFadiga):
    dados_alerta = alerta.model_dump()
    dados_alerta["timestamp"] = datetime.now().strftime("%H:%M:%S")
    alertas_ativos[alerta.veiculo_id] = dados_alerta
    return {"status": "sucesso"}

@app.get("/api/alertas-atuais")
async def obtener_alertas():
    return list(alertas_ativos.values())

if __name__ == "__main__":
    import uvicorn
=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse # <-- NOVO
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(title="Sistema de Monitoramento de Fadiga - Polícia")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlertaFadiga(BaseModel):
    veiculo_id: str
    motorista_nome: str
    nivel_fadiga: str  
    ear_valor: float   
    bocejos: int       

alertas_ativos = {}

# --- [NOVA ROTA] Serve a Dashboard Web para a Polícia ---
# --- [ATUALIZADO] Serve a Dashboard Web usando caminhos absolutos ---
@app.get("/", response_class=HTMLResponse)
async def obter_dashboard():
    # Descobre a pasta onde o server.py está guardado
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    # Junta com a pasta templates e o ficheiro html
    caminho_html = os.path.join(diretorio_atual, "template", "dashboard.html")
    
    with open(caminho_html, "r", encoding="utf-8") as ficheiro:
        return ficheiro.read()

@app.post("/api/alerta")
async def receber_alerta(alerta: AlertaFadiga):
    dados_alerta = alerta.model_dump()
    dados_alerta["timestamp"] = datetime.now().strftime("%H:%M:%S")
    alertas_ativos[alerta.veiculo_id] = dados_alerta
    return {"status": "sucesso"}

@app.get("/api/alertas-atuais")
async def obtener_alertas():
    return list(alertas_ativos.values())

if __name__ == "__main__":
    import uvicorn
>>>>>>> 9a7c08abd99ef3093a3f100db9cdb62dea1a3d8c
    uvicorn.run(app, host="0.0.0.0", port=8000)