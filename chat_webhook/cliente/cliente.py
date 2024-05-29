import requests
from flask import Flask, request, jsonify
import threading
import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

app = Flask(__name__)

# URL do servidor
url_servidor = 'http://127.0.0.1:5000'

def encontrar_porta_livre(porta_inicial):
    porta = porta_inicial
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', porta)) != 0:
                return porta
            porta += 1

def executar_cliente(porta):
    app.run(host='127.0.0.1', port=porta)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    mensagem = data.get('message')
    print(f"Mensagem criptografada recebida: {mensagem}")
    mensagem_descriptografada = descriptografar_mensagem(mensagem)
    print(f"Mensagem recebida: {mensagem_descriptografada}")
    return jsonify({"message": "Mensagem recebida"}), 200

def registrar_no_servidor(porta):
    url = f'http://127.0.0.1:{porta}/webhook'
    try:
        requests.post(f'{url_servidor}/register', json={'url': url})
        print(f"Registrado no servidor em {url_servidor}")
    except requests.exceptions.RequestException as e:
        print(f"Falha ao registrar no servidor: {e}")

def enviar_mensagem(porta):
    mensagem = input("")
    mensagem_criptografada = criptografar_mensagem(mensagem)
    try:
        requests.post(f'{url_servidor}/message', json={'message': mensagem_criptografada, 'sender': f'http://127.0.0.1:{porta}/webhook'})
    except requests.exceptions.RequestException as e:
        print(f"Falha ao enviar a mensagem: {e}")

def carregar_chave_publica():
    with open("C:\\Users\\Ale\\Desktop\\chat_webhook\\cliente\\public_key.pem", "rb") as key_file:
        chave_publica = serialization.load_pem_public_key(key_file.read())
    return chave_publica

def carregar_chave_privada():
    with open("C:\\Users\\Ale\\Desktop\\chat_webhook\\cliente\\private_key.pem", "rb") as key_file:
        chave_privada = serialization.load_pem_private_key(key_file.read(), password=None)
    return chave_privada

def criptografar_mensagem(mensagem):
    chave_publica = carregar_chave_publica()
    mensagem_criptografada = chave_publica.encrypt(
        mensagem.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensagem_criptografada.hex()

def descriptografar_mensagem(mensagem_criptografada):
    chave_privada = carregar_chave_privada()
    mensagem_criptografada_bytes = bytes.fromhex(mensagem_criptografada)
    mensagem = chave_privada.decrypt(
        mensagem_criptografada_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensagem.decode()

if __name__ == '__main__':
    porta_inicial = 5001
    porta_cliente = encontrar_porta_livre(porta_inicial)
    
    threading.Thread(target=executar_cliente, args=(porta_cliente,)).start()
    registrar_no_servidor(porta_cliente)
    
    while True:
        enviar_mensagem(porta_cliente)
