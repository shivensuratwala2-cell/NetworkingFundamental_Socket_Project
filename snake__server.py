import socket
import threading

# Server Configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5555
clients = []
player_positions = {} # {addr: [x, y]}

def broadcast(message, _client):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            clients.remove(client)

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    player_positions[str(addr)] = [0, 0] # Start at top-left
    
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if not msg: break
            
            # Additional Feature: Group Chat
            if msg.startswith("CHAT:"):
                broadcast(f"CHAT from {addr}: {msg[5:]}", client)
            
            # Game Logic: Movement
            elif msg in ['w', 'a', 's', 'd']:
                pos = player_positions[str(addr)]
                if msg == 'w': pos[1] -= 1
                if msg == 's': pos[1] += 1
                if msg == 'a': pos[0] -= 1
                if msg == 'd': pos[0] += 1
                broadcast(f"MOVE:{addr}:{pos[0]}:{pos[1]}", client)
        except:
            break

    clients.remove(client)
    client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server started on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

def handle_client(client, addr):
    while True:
        try:
            raw_msg = client.recv(1024).decode('utf-8')
            if not raw_msg: break
            
            # Split the message into Name and Command
            # Format: NAME:John|CMD:w
            parts = raw_msg.split('|')
            p_name = parts[0].replace("NAME:", "")
            p_cmd = parts[1].replace("CMD:", "")
            
            if p_cmd.startswith("CHAT:"):
                # Broadcast showing the entered name
                broadcast(f"[{p_name}]: {p_cmd[5:]}", client)
            
            elif p_cmd in ['w', 'a', 's', 'd']:
                # ... existing movement logic ...
                broadcast(f"{p_name} moved to {new_pos}", client)
        except:
            break
