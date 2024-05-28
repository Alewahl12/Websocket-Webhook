import requests
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Carregar a chave pública
with open("C:\\Users\\Ale\\Desktop\\Webhook2\\loja\\public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read())

#Para facilitar
lista_compra = {
    'Nome': "Pedro",
    'Cartao': "1111222233334444",
    'Item': "Bola",
    'Valor': "100"
}

compra_finalizada = False

while not compra_finalizada:
    op = input("Deseja finalizar a compra? S/N\n")
    if op.upper() == 'S':
        compra_finalizada = True

if compra_finalizada:
    # Serializar e criptografar os dados
    compra_serializada = json.dumps(lista_compra).encode('utf-8')
    compra_criptografada = public_key.encrypt(
        compra_serializada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Enviar os dados criptografados
    response = requests.post("http://localhost:5000/receber_compra", data=compra_criptografada)
    if response.status_code == 200:
        print("Compra finalizada com sucesso")
    else:
        print(f"Falha ao enviar a compra. Código de status: {response.status_code}")
