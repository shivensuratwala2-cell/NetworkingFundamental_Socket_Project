import socket
import threading
import time

# Core Settings
HOST = '172.16.17.147'
PORT = 1234
MAX_PLAYERS = 3
GRID_SIZE = 10



import random  # <--- CRITICAL: This fix resolves your NameError




# Game State
players = [] 
current_turn = 0
key_pos = [random.randint(0, 9), random.randint(0, 9)]
door_pos = [random.randint(0, 9), random.randint(0, 9)]
has_key = False

def get_map_string():
    """Renders the 10x10 escape room layout"""
    display_size = 10
    grid = [[" . " for _ in range(display_size)] for _ in range(display_size)]
    for p in players:
        px, py = p["pos"][0] % display_size, p["pos"][1] % display_size
        grid[py][px] = f"[{p['name'][0].upper()}]"
    
    if has_key: grid[door_pos[1]][door_pos[0]] = " D "
        
    map_render = "\n--- ESCAPE ROOM LAYOUT ---\n"
    for row in grid:
        map_render += "".join(row) + "\n"
    map_render += "STATUS: " + ("Key found! Go to Door (D)" if has_key else "Find the Key!")
    return map_render

def broadcast(msg):
    """Sends messages to all connected clients"""
    for p in players:
        try: p["conn"].send(msg.encode('utf-8'))
        except: pass

def broadcast_turn_status():
    """Identifies the active player and updates the screen"""
    global current_turn
    layout = get_map_string()
    active_name = players[current_turn]["name"]
    for i, p in enumerate(players):
        try:
            p["conn"].send("\033[H\033[J".encode('utf-8')) # Clear screen command
            p["conn"].send(layout.encode('utf-8'))
            if i == current_turn:
                p["conn"].send(f"\n*** YOUR TURN, {p['name'].upper()}! (w/a/s/d or chat:msg) ***\n".encode('utf-8'))
            else:
                p["conn"].send(f"\nWaiting for {active_name} to move...\n".encode('utf-8'))
        except: pass

def handle_client(conn, addr, index):
    global current_turn, has_key
    print(f"[STATUS] Player {index+1} connected from {addr}")
    
    try:
        conn.send("WELCOME! Enter Name: ".encode('utf-8'))
        name = conn.recv(1024).decode('utf-8').strip()
        players.append({"conn": conn, "name": name, "pos": [index*2, index*2]})
        
        while len(players) < MAX_PLAYERS:
            conn.send(f"Waiting for {MAX_PLAYERS - len(players)} more members...".encode('utf-8'))
            time.sleep(2)

        broadcast_turn_status()

        while True:
            msg = conn.recv(1024).decode('utf-8').strip().lower()
            if current_turn == index:
                if msg in ['w', 'a', 's', 'd']:
                    p_pos = players[index]["pos"]
                    if msg == 'w': p_pos[1] = (p_pos[1] - 1) % GRID_SIZE
                    if msg == 's': p_pos[1] = (p_pos[1] + 1) % GRID_SIZE
                    if msg == 'a': p_pos[0] = (p_pos[0] - 1) % GRID_SIZE
                    if msg == 'd': p_pos[0] = (p_pos[0] + 1) % GRID_SIZE
                    
                    if p_pos == key_pos and not has_key:
                        has_key = True
                        broadcast("\n!!! SYSTEM: KEY FOUND !!!\n")
                    
                    if p_pos == door_pos and has_key:
                        broadcast("\nVICTORY! YOU ESCAPED THE ROOM!\n")
                        break

                    current_turn = (current_turn + 1) % MAX_PLAYERS
                    broadcast_turn_status()
                elif msg.startswith("chat:"):
                    broadcast(f"CHAT [{name}]: {msg[5:]}")
    except: pass
    finally: conn.close()

# Start Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((HOST, PORT))
    server.listen(MAX_PLAYERS)
    print(f"[SERVER ONLINE] Listening on {HOST}:{PORT}")
except Exception as e:
    print(f"[ERROR] Binding failed: {e}")
    exit()

conn_count = 0
while conn_count < MAX_PLAYERS:
    c, addr = server.accept()
    threading.Thread(target=handle_client, args=(c, addr, conn_count)).start()
    conn_count += 1
