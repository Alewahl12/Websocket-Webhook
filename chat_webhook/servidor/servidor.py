#servidor.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Lista para armazenar as URLs dos clientes
client_urls = []

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    url = data.get('url')
    if url and url not in client_urls:
        client_urls.append(url)
    return jsonify({"message": "Cliente registrado"}), 200

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    mensagem = data.get('message')
    remetente = data.get('sender')

    print(f"{remetente} enviou a mensagem criptografada: {mensagem}")
    
    if mensagem:
        for url in client_urls:
            if url != remetente:  # envia para todos menos o remetente
                try:
                    requests.post(url, json={'message': mensagem})
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao enviar a mensagem para {url}: {e}")
    
    return jsonify({"message": "Mensagem recebida"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
