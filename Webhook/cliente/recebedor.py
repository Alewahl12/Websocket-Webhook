from flask import Flask, request
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import json

app = Flask(__name__)

# Carregar a chave privada
with open("C:\\Users\\Ale\\Desktop\\Webhook2\\cliente\\private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None)

@app.route('/notificar', methods=['POST'])
def notificar():
    dados_criptografados = request.data
    print(f"Notificacao criptografada: {dados_criptografados}")

    # Descriptografa os dados
    dados_serializados = private_key.decrypt(
        dados_criptografados,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Desserializa os dados
    dados = json.loads(dados_serializados.decode('utf-8'))
    mensagem = f"{dados['Nome']} comprou seu(a) {dados['Item']} no valor de {dados['Valor']} R$"
    print(f"Mensagem recebida: {mensagem}")
    return '', 200

if __name__ == '__main__':
    app.run(port=5001)
