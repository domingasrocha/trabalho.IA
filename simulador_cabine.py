import requests
import time
import random

API_URL = "http://localhost:8000/api/alerta"
MATRICULA = "LD-82-45-AM"
MOTORISTA = "Elisio (Simulado)"

# Atenção: Sem acentos para evitar incompatibilidade de caracteres no JSON
estados_possiveis = ["Normal", "Alerta", "Critico"]

print("[*] Simulador da Cabine Ativo. Enviando dados...")

try:
    while True:
        # Garante que escolhe um estado NOVO a cada ciclo!
        nivel_teste = random.choice(estados_possiveis)
        
        dados_teste = {
            "veiculo_id": MATRICULA,
            "motorista_nome": MOTORISTA,
            "nivel_fadiga": nivel_teste, 
            "ear_valor": 0.0,
            "bocejos": random.randint(0, 4)
        }
        
        try:
            requests.post(API_URL, json=dados_teste, timeout=1)
            print(f"[ENVIO] Enviado: -> {nivel_teste}")
        except requests.exceptions.RequestException:
            print("[ERRO] Server.py offline.")
            
        time.sleep(2) # Envia a cada 2 segundos

except KeyboardInterrupt:
    print("\n[*] Simulador parado.")