# Websocket-Webhook

WebSocket Chat com Criptografia RSA
Este projeto demonstra a implementação de um chat WebSocket em Python com criptografia RSA. As mensagens são criptografadas usando uma chave pública antes de serem enviadas e descriptografadas no cliente destinatário usando a chave privada correspondente.

Arquivos
Servidor
servidor.py

python
Copiar código
import asyncio
import websockets
import logging

logging.basicConfig(level=logging.INFO)

connected_clients = {}
client_id_counter = 0

async def handler(websocket, path):
    global connected_clients, client_id_counter
    client_id_counter += 1
    client_id = client_id_counter
    connected_clients[websocket] = client_id
    logging.info(f"Client {client_id} connected")

    try:
        async for message in websocket:
            logging.info(f"Received message from Client {client_id}: {message}")
            # Enviar a mensagem para todos os clientes conectados, exceto o remetente
            await asyncio.gather(*[
                client.send(message)
                for client in connected_clients if client != websocket
            ])
    except websockets.exceptions.ConnectionClosed:
        logging.info(f"Client {client_id} disconnected")
    finally:
        del connected_clients[websocket]

async def main():
    start_server = await websockets.serve(handler, "localhost", 5000)
    logging.info("Server started on ws://localhost:5000")
    await start_server.wait_closed()

asyncio.run(main())
Cliente
cliente.py

python
Copiar código
import asyncio
from websockets.client import connect
import websockets.exceptions
import aioconsole
import logging
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

logging.basicConfig(level=logging.INFO)

# Carregar chave pública para criptografar mensagens
with open("C:\\Users\\Ale\\Desktop\\Websocket\\cliente\\public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Carregar chave privada para descriptografar mensagens
with open("C:\\Users\\Ale\\Desktop\\Websocket\\cliente\\private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

async def chat():
    try:
        async with connect("ws://localhost:5000", ping_interval=10, ping_timeout=20) as websocket:
            logging.info("Conectado ao servidor WebSocket")
            
            async def send_message():
                while True:
                    message = await aioconsole.ainput("")
                    if message.lower() == "sair":
                        logging.info("Encerrando a conexão")
                        await websocket.close()
                        break
                    encrypted_message = public_key.encrypt(
                        message.encode(),
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    await websocket.send(encrypted_message)

            async def receive_message():
                try:
                    while True:
                        response = await websocket.recv()
                        try:
                            decrypted_message = private_key.decrypt(
                                response,
                                padding.OAEP(
                                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                    algorithm=hashes.SHA256(),
                                    label=None
                                )
                            )
                            print(f"Mensagem recebida: {decrypted_message.decode()}")
                        except Exception as e:
                            logging.error(f"Erro ao descriptografar a mensagem: {e}")
                except websockets.exceptions.ConnectionClosed:
                    logging.info("Conexão fechada pelo servidor")

            await asyncio.gather(send_message(), receive_message())
    except websockets.exceptions.ConnectionClosed as e:
        logging.error(f"Connection closed: {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")

asyncio.run(chat())
Funcionamento
Servidor:

Inicia um servidor WebSocket na porta 5000.
Mantém uma lista de clientes conectados.
Retransmite mensagens recebidas para todos os clientes, exceto o remetente.
Cliente:

Conecta ao servidor WebSocket.
Criptografa mensagens com uma chave pública antes de enviá-las.
Recebe mensagens criptografadas e as descriptografa usando uma chave privada.
Requisitos
Python 3.7 ou superior
Bibliotecas:
websockets
aioconsole
cryptography
Instruções
Instale as bibliotecas necessárias:

bash
Copiar código
pip install websockets aioconsole cryptography
Gere um par de chaves RSA (public_key.pem e private_key.pem).

Execute o servidor:

bash
Copiar código
python servidor.py
Execute um ou mais clientes:

bash
Copiar código
python cliente.py
No cliente, digite mensagens para enviar ao servidor. As mensagens serão criptografadas, enviadas ao servidor e retransmitidas para outros clientes conectados, que irão descriptografá-las e exibi-las.
