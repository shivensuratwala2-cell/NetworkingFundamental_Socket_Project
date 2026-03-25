import socket
import threading
import time
import random

# --- SETTINGS ---
HOST = '0.0.0.0' 
PORT = 1234
MAX_PLAYERS = 0 
GRID_SIZE = 10 

# --- GAME STATE ---
players = [] 
current_turn = 0
key_pos = [random.randint(0, 9), random.randint(0, 9)]
door_pos = [random.randint(0, 9), random.randint(0, 9)]
has_key = False
start_time = None
game_active = True

def get_map_string():
    """Renders a pixel-perfect aligned terminal UI"""
    elapsed = int(time.time() - start_time) if start_time else 0
    mins, secs = divmod(elapsed, 60)
    time_str = f"{mins:02d}:{secs:02d}"

    # Initialize grid with 3-character wide dots
    grid = [[" . " for _ in range(10)] for _ in range(10)]
    
    # K and D must be 3 characters wide (" K " / " D ") to maintain alignment
    if not has_key:
        grid[key_pos[1]][key_pos[0]] = " K "
    else:
        grid[door_pos[1]][door_pos[0]] = " D "

    for p in players:
        px, py = p["pos"][0] % 10, p["pos"][1] % 10
        grid[py][px] = f"[{p['name'][0].upper()}]"

    # --- UI CONSTRUCTION (FIXED ALIGNMENT) ---
    # content_width is 30 (10 columns * 3 chars) + 2 spaces = 32
    border_top    = "╔" + "═" * 32 + "╗"
    border_mid    = "╠" + "═" * 32 + "╣"
    border_bottom = "╚" + "═" * 32 + "╝"
    
    # Centering the time header
    header_text = f"║ {f'ESCAPE ROOM | TIME: {time_str}':^30} ║\n"
    
    map_body = ""
    for row in grid:
        map_body += "║ " + "".join(row) + " ║\n"
    
    # FIXED: The Mission Status is now perfectly centered within 30 characters
    status_msg = "MISSION: SECURE EXIT (D)" if has_key else "MISSION: LOCATE DATA KEY (K)"
    footer_text = f"║ {status_msg:^30} ║\n"
    
    return f"\n{border_top}\n{header_text}{border_mid}\n{map_body}{border_mid}\n{footer_text}{border_bottom}\n"
def broadcast(msg):
    for p in players:
        try: p["conn"].send(msg.encode('utf-8'))
        except: pass

def broadcast_turn_status():
    global current_turn
    layout = get_map_string()
    active_name = players[current_turn]["name"]
    for i, p in enumerate(players):
        try:
            p["conn"].send("\033[H\033[J".encode('utf-8')) 
            p["conn"].send(layout.encode('utf-8'))
            if i == current_turn:
                p["conn"].send(f"\n>>> ACCESS GRANTED: YOUR TURN, {p['name'].upper()}! <<<\n".encode('utf-8'))
            else:
                p["conn"].send(f"\nWaiting for {active_name} to authorize movement...\n".encode('utf-8'))
        except: pass

def handle_client(conn, addr, index):
    global current_turn, has_key, start_time, game_active, MAX_PLAYERS
    try:
        if index == 0:
            conn.send("SYSTEM_ADMIN: Set Total Authorized Agents (1-4): ".encode('utf-8'))
            choice = conn.recv(1024).decode().strip()
            MAX_PLAYERS = int(choice) if choice in ['1','2', '3', '4'] else 3

        conn.send("INPUT AGENT CREDENTIALS (Name): ".encode('utf-8'))
        name = conn.recv(1024).decode().strip()
        players.append({"conn": conn, "name": name, "pos": [random.randint(0,2), random.randint(0,2)]})
        
        while len(players) < MAX_PLAYERS:
            conn.send(f"\n[SCANNING] Waiting for {MAX_PLAYERS - len(players)} more agents...".encode('utf-8'))
            time.sleep(2)

        if not start_time: start_time = time.time()
        broadcast_turn_status()

        while game_active:
            msg = conn.recv(1024).decode().strip().lower()
            if not msg: break
            
            if current_turn == index:
                pos = players[index]["pos"]
                if msg == 'w': pos[1] = (pos[1]-1)%10
                elif msg == 's': pos[1] = (pos[1]+1)%10
                elif msg == 'a': pos[0] = (pos[0]-1)%10
                elif msg == 'd': pos[0] = (pos[0]+1)%10
                
                if pos == key_pos and not has_key:
                    has_key = True
                    broadcast("\n[ALERT] DATA KEY SECURED BY AGENT " + name.upper() + "\n")
                
                if pos == door_pos and has_key:
                    final_elapsed = int(time.time() - start_time)
                    broadcast(f"\n⚡ MISSION SUCCESS! PROTOCOL COMPLETE IN {final_elapsed}s! ⚡\n")
                    game_active = False
                    time.sleep(5) 
                    break
                
                current_turn = (current_turn + 1) % MAX_PLAYERS
                broadcast_turn_status()
    except: pass
    finally: conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(4)
print(f"Final Aesthetic Server online on {PORT}")

conn_count = 0
while True:
    c, addr = server.accept()
    threading.Thread(target=handle_client, args=(c, addr, conn_count)).start()
    conn_count += 1
    if MAX_PLAYERS > 0 and conn_count >= MAX_PLAYERS: break
