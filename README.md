WebSocket Chat com Criptografia RSA
Este projeto demonstra um chat em tempo real utilizando WebSockets com mensagens criptografadas usando RSA.

Como Funciona
Servidor (servidor.py):

Inicia um servidor WebSocket na porta 5000.
Mantém uma lista de clientes conectados.
Recebe mensagens de um cliente e as retransmite para todos os outros clientes conectados.
Cliente (cliente.py):

Conecta ao servidor WebSocket.
Criptografa mensagens com uma chave pública antes de enviá-las.
Recebe mensagens criptografadas, as descriptografa usando uma chave privada, e exibe o conteúdo.
Requisitos
Python 3.7 ou superior
Bibliotecas: websockets, aioconsole, cryptography
Instruções
Instale as bibliotecas necessárias:

pip install websockets aioconsole cryptography

Execute o servidor em um terminal:
python servidor.py

Execute um ou mais clientes:

python cliente.py

No cliente, digite mensagens para enviar ao servidor. As mensagens serão criptografadas, enviadas ao servidor e retransmitidas para outros clientes conectados, que irão descriptografá-las e exibi-las.

Este projeto é uma demonstração de como implementar criptografia RSA em um chat em tempo real usando WebSockets.




