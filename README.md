# Participantes
> Alexandre Henning Wahl
> Felipe Porto Caldeira do Nascimento

# WebSocket Chat com Criptografia RSA

Este projeto demonstra um chat em tempo real utilizando WebSockets com mensagens criptografadas usando RSA.

## Como Funciona

1. **Servidor (`servidor.py`)**:
   - Inicia um servidor WebSocket na porta 5000.
   - Mantém uma lista de clientes conectados.
   - Recebe mensagens de um cliente e as retransmite para todos os outros clientes conectados.

2. **Cliente (`cliente.py`)**:
   - Conecta ao servidor WebSocket.
   - Criptografa mensagens com uma chave pública antes de enviá-las.
   - Recebe mensagens criptografadas, as descriptografa usando uma chave privada, e exibe o conteúdo.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas: `websockets`, `aioconsole`, `cryptography`

## Instruções

1. Instale as bibliotecas necessárias:
   ```bash
   pip install websockets aioconsole cryptography

2. Execute o servidor em um terminal:

   ```bash
      python servidor.py

3. Execute um ou mais clientes:

   ```bash
      python cliente.py

No cliente, digite mensagens para enviar ao servidor. As mensagens serão criptografadas, enviadas ao servidor e retransmitidas para outros clientes conectados, que irão descriptografá-las e exibi-las.


# Sistema Webhook de Notificação de Compra com Criptografia RSA

Este projeto demonstra um sistema webhook para notificação de compra, utilizando Flask para os servidores e criptografia RSA para proteger os dados.

## Como Funciona

1. **Cliente de Compra (`compra.py`)**:
   - Coleta os dados da compra do usuário.
   - Criptografa os dados usando uma chave pública (`public_key.pem`).
   - Envia os dados criptografados ao servidor intermediário.

2. **Servidor Intermediário (`servidor.py`)**:
   - Recebe os dados criptografados do cliente de compra.
   - Repassa os dados criptografados ao servidor de notificação.

3. **Servidor de Notificação (`recebedor.py`)**:
   - Recebe os dados criptografados do servidor intermediário.
   - Descriptografa os dados usando uma chave privada (`private_key.pem`).
   - Exibe uma mensagem formatada de notificação.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas: `flask`, `requests`, `cryptography`

## Instruções

1. Instale as bibliotecas necessárias:
   ```bash
   pip install flask requests cryptography

2. Execute os scripts em diferentes terminais:

   Servidor de Notificação (recebedor.py):
      ```bash
      python recebedor.py
      ```

   Servidor Intermediário (servidor.py):
      ```bash
      python servidor.py
      ```

   Cliente de Compra (compra.py):
      ```bash
      python compra.py
      ```
