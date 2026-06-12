import cv2
import numpy as np
import socket
import json
import threading

dados_central = {
    "matricula": "---",
    "rota": "Nenhuma rota ativa",
    "nivel": "VERDE",
    "status": "SISTEMA OPERACIONAL",
    "timestamp": "--:--:--"
}
cor_painel = (0, 150, 0)

def escutar_veiculos():
    global dados_central, cor_painel
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 5000))
    servidor.listen(5)
    
    while True:
        conexao, endereco = servidor.accept()
        mensagem = conexao.recv(1024).decode('utf-8')
        if mensagem:
            dados_recebidos = json.loads(mensagem)
            dados_central = dados_recebidos
            
            # Atualiza a cor do dashboard na central da polícia com base no nível enviado pelo carro
            if dados_central["nivel"] == "VERMELHO":
                cor_painel = (0, 0, 255)     # Vermelho (Crítico)
            elif dados_central["nivel"] == "AMARELO":
                cor_painel = (0, 200, 255)   # Amarelo (Aviso Preventivo)
            else:
                cor_painel = (0, 150, 0)     # Verde (Normalizado)
                
        conexao.close()

def iniciar_dashboard_policia():
    print("[*] Iniciando Painel de Fiscalização Rodoviária da Polícia...")
    
    thread_rede = threading.Thread(target=escutar_veiculos, daemon=True)
    thread_rede.start()
    
    dashboard = np.zeros((600, 900, 3), dtype=np.uint8)
    
    while True:
        dashboard[:] = (30, 30, 30)
        
        # 1. Barra de Título
        cv2.rectangle(dashboard, (0, 0), (900, 80), (50, 50, 50), -1)
        cv2.putText(dashboard, "POLÍCIA NACIONAL - MONITORIZAÇÃO DE SINAIS VITAIS RODOVIÁRIOS", (30, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        
        # 2. Painel Dinâmico de Alerta Central
        cv2.rectangle(dashboard, (30, 110), (870, 190), cor_painel, -1)
        
        # Cor do texto do status muda para preto se for amarelo para melhor legibilidade
        cor_texto_status = (0, 0, 0) if dados_central["nivel"] == "AMARELO" else (255, 255, 255)
        cv2.putText(dashboard, f"STATUS: {dados_central['status']}", (50, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_texto_status, 3)
        
        # 3. Informações de Rastreabilidade do Alvo
        cv2.rectangle(dashboard, (30, 220), (870, 530), (40, 40, 40), -1)
        
        cv2.putText(dashboard, f"Matrícula Monitorizada: {dados_central['matricula']}", (60, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (240, 240, 240), 2)
                    
        cv2.putText(dashboard, f"Itinerário do Veículo: {dados_central['rota']}", (60, 350),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (190, 190, 190), 2)
                    
        cv2.putText(dashboard, f"Registo de Transmissão: {dados_central['timestamp']}", (60, 420),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (190, 190, 190), 2)
        
        # 4. Diretrizes operacionais para a polícia dependendo do nível
        if dados_central["nivel"] == "VERMELHO":
            cv2.putText(dashboard, "DIRETRIZ: PERIGO CRÍTICO! Intercetar veículo imediatamente.", (60, 490),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)
        elif dados_central["nivel"] == "AMARELO":
            cv2.putText(dashboard, "DIRETRIZ: Alerta preventivo. Monitorizar deslocamento via radar.", (60, 490),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        else:
            cv2.putText(dashboard, "DIRETRIZ: Fluxo rodoviário regular. Nenhuma ação pendente.", (60, 490),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 255, 150), 1)

        cv2.putText(dashboard, "Pressione 'ESC' para fechar a central de comando.", (30, 575),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120, 120, 120), 1)

        cv2.imshow("MININT - Painel de Comando Remoto", dashboard)
        
        if cv2.waitKey(30) & 0xFF == 27:
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_dashboard_policia()