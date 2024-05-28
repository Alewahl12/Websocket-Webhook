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
