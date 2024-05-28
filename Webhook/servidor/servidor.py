from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/receber_compra', methods=['POST'])
def receber_compra():
    dados_criptografados = request.data
    print(f"Dados recebidos: {dados_criptografados}")

    # Repassa os dados criptografados ao recebedor.py
    response = requests.post("http://localhost:5001/notificar", data=dados_criptografados)
    if response.status_code == 200:
        print("Dados repassados com sucesso")
    else:
        print(f"Falha ao repassar os dados. Código de status: {response.status_code}")

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
