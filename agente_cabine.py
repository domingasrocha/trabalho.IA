import cv2
import numpy as np
import requests  
import time      
import socket
import json
import os

def notificar_central_remota(matricula, rota, nivel, status):
    """Envia o nível de fadiga em tempo real para a Central da Polícia via Sockets (Mantido)"""
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('localhost', 5000))
        
        dados = {
            "matricula": matricula,
            "rota": rota,
            "nivel": nivel, 
            "status": status,
            "timestamp": time.strftime("%H:%M:%S")
        }
        
        cliente.send(json.dumps(dados).encode('utf-8'))
        cliente.close()
    except ConnectionRefusedError:
        pass 

def rodar_agente_cabine():
    MATRICULA = "LD-82-45-AM"
    ROTA = "Luanda -> Benguela (EN100)"
    MOTORISTA = "Domingas"  # Teu nome para aparecer na API
    
    print(f"[*] Sistema Híbrido Ativo no Veículo [{MATRICULA}].")
    print("[*] Usando Algoritmo de Cascata de Haars (OpenCV Puro).")

    # Carregar os detetores localmente a partir da pasta do projeto
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    
    # Limiares de tempo baseados em frames para os alertas
    FRAMES_AMARELO = 10   
    FRAMES_VERMELHO = 25  
    
    contador_frames_sem_olhos = 0
    nivel_atual = "VERDE"
    ultimo_nivel_notificado = "VERDE"

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO CRÍTICO] Câmara de monitorização da cabine não encontrada.")
        return

    # Janela de sinalização do motorista (Semáforo de atenção)
    tela_sinalizacao = np.zeros((300, 500, 3), dtype=np.uint8)
    
    # --- [ADICIONADO] CONFIGURAÇÃO DA API FASTAPI DA POLÍCIA ---
    API_URL = "http://localhost:8000/api/alerta"
    ultimo_envio_api = time.time()
    ultimo_nivel_enviado_api = ""

    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            continue

        # Transforma em escala de cinzentos
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detetar o rosto do motorista
        rostos = face_cascade.detectMultiScale(cinza, 1.3, 5)
        
        olhos_detetados_no_frame = False

        for (x, y, w, h) in rostos:
            roi_cinza = cinza[y:y+h, x:x+w]
            olhos = eye_cascade.detectMultiScale(roi_cinza, 1.1, 4)
            
            if len(olhos) >= 1:
                olhos_detetados_no_frame = True
                break 

        # Máquina de Estados baseada na ausência dos olhos
        if not olhos_detetados_no_frame and len(rostos) > 0:
            contador_frames_sem_olhos += 1
            if contador_frames_sem_olhos >= FRAMES_VERMELHO:
                nivel_atual = "VERMELHO"
            elif contador_frames_sem_olhos >= FRAMES_AMARELO:
                nivel_atual = "AMARELO"
        else:
            contador_frames_sem_olhos = 0
            nivel_atual = "VERDE"

        # Gestão de Notificações para a Polícia Nacional (Via Sockets)
        if nivel_atual != ultimo_nivel_notificado:
            if nivel_atual == "AMARELO":
                notificar_central_remota(MATRICULA, ROTA, "AMARELO", "CONDUTOR COM EXAUSTÃO/DISTRAÇÃO")
            elif nivel_atual == "VERMELHO":
                notificar_central_remota(MATRICULA, ROTA, "VERMELHO", "PERIGO: CONDUTOR A DORMIR AO VOLANTE!")
            elif nivel_atual == "VERDE" and ultimo_nivel_notificado in ["AMARELO", "VERMELHO"]:
                notificar_central_remota(MATRICULA, ROTA, "VERDE", "SITUAÇÃO NORMALIZADA")
            
            ultimo_nivel_notificado = nivel_atual

        # -------------------------------------------------------------
        # [ADICIONADO] LÓGICA DE ENVIO PARA O NOSSO BACK-END FASTAPI
        # -------------------------------------------------------------
        tempo_atual = time.time()
        
        # Mapeia as cores para o formato de texto que o servidor espera
        status_map = {"VERDE": "Normal", "AMARELO": "Alerta", "VERMELHO": "Critico"}
        nivel_formatado = status_map.get(nivel_atual, "Normal")

        # Envia a cada 2 segundos OU imediatamente se mudar para VERMELHO (Crítico)
        if (tempo_atual - ultimo_envio_api > 2.0) or (nivel_atual == "VERMELHO" and ultimo_nivel_enviado_api != "VERMELHO"):
            dados_api = {
                "veiculo_id": MATRICULA,        # Usa a matrícula que já definiste
                "motorista_nome": MOTORISTA,
                "nivel_fadiga": nivel_formatado, # "Normal", "Alerta" ou "Critico"
                "ear_valor": 0.0,                # Como usas Haar Cascades puro, enviamos 0.0 fixo (não usa EAR geométrico)
                "bocejos": 0                     # Inicializado a zero
            }
            try:
                # Envio HTTP rápido via POST
                requests.post(API_URL, json=dados_api, timeout=0.4)
                ultimo_envio_api = tempo_atual
                ultimo_nivel_enviado_api = nivel_atual
            except requests.exceptions.RequestException:
                pass # Se o server.py estiver fechado, não trava o loop da câmara

        # Atualizar a Interface Visual do Motorista (O Semáforo na cabine)
        if nivel_atual == "VERDE":
            tela_sinalizacao[:] = (0, 150, 0) 
            texto_hud = "ATENCAO: OK"
            cor_texto = (255, 255, 255)
        elif nivel_atual == "AMARELO":
            tela_sinalizacao[:] = (0, 200, 255) 
            texto_hud = "AVISO: RECOMPONHA-SE!"
            cor_texto = (0, 0, 0)
        elif nivel_atual == "VERMELHO":
            cor_pisca = (0, 0, 255) if int(time.time() * 5) % 2 == 0 else (0, 0, 50)
            tela_sinalizacao[:] = cor_pisca
            texto_hud = "PERIGO: PARE O VEICULO!"
            cor_texto = (255, 255, 255)

        cv2.putText(tela_sinalizacao, texto_hud, (40, 160), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, cor_texto, 3)
        
        cv2.imshow("Painel de Alerta do Condutor", tela_sinalizacao)

        # Fecha com ESC
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    rodar_agente_cabine()