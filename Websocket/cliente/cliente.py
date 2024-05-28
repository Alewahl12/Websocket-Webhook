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
                        #print(f"{response}")
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
