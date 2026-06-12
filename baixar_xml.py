<<<<<<< HEAD
import urllib.request

urls = {
    "haarcascade_frontalface_default.xml": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml",
    "haarcascade_eye_tree_eyeglasses.xml": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml"
}

print("[*] Iniciando download dos classificadores limpos...")

for nome, url in urls.items():
    try:
        # Força o download do arquivo puro (RAW)
        urllib.request.urlretrieve(url, nome)
        print(f"[SUCESSO] Ficheiro '{nome}' descarregado corretamente.")
    except Exception as e:
        print(f"[ERRO] Falha ao descarregar {nome}: {e}")

=======
import urllib.request

urls = {
    "haarcascade_frontalface_default.xml": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml",
    "haarcascade_eye_tree_eyeglasses.xml": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml"
}

print("[*] Iniciando download dos classificadores limpos...")

for nome, url in urls.items():
    try:
        # Força o download do arquivo puro (RAW)
        urllib.request.urlretrieve(url, nome)
        print(f"[SUCESSO] Ficheiro '{nome}' descarregado corretamente.")
    except Exception as e:
        print(f"[ERRO] Falha ao descarregar {nome}: {e}")

>>>>>>> 9a7c08abd99ef3093a3f100db9cdb62dea1a3d8c
print("[*] Processo concluído.")