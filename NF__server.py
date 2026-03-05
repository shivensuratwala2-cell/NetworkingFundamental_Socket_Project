import socket
import threading
import time

# Core Settings
HOST = '172.16.17.147'
PORT = 1234
MAX_PLAYERS = 3
GRID_SIZE = 10



import random



# Game State
players = [] 
current_turn = 0
# Randomized hidden locations for the key and door
key_pos = [random.randint(0, 9), random.randint(0, 9)]
door_pos = [random.randint(0, 9), random.randint(0, 9)]
has_key = False
winner_name = None

def get_map_string():
    display_size = 10
    grid = [[" . " for _ in range(display_size)] for _ in range(display_size)]
    
    # Place players on grid
    for p in players:
        px, py = p["pos"][0] % display_size, p["pos"][1] % display_size
        grid[py][px] = f"[{p['name'][0].upper()}]"
    
    # Optional: Show door if you want players to see the goal
    grid[door_pos[1]][door_pos[0]] = " D "
        
    map_render = "\n--- ESCAPE ROOM LAYOUT ---\n"
    for row in grid:
        map_render += "".join(row) + "\n"
    
    if has_key:
        map_render += f"STATUS: Key found! Get to the Door (D)!\n"
    else:
        map_render += "STATUS: Search for the hidden Key!\n"
    return map_render

# ... (keep broadcast() and broadcast_turn_status() as they are)

def handle_client(conn, index):
    global current_turn, has_key, winner_name
    try:
        conn.send("WELCOME TO ESCAPE ROOM! Enter Name: ".encode('utf-8'))
        name = conn.recv(1024).decode('utf-8').strip()
        players.append({"conn": conn, "name": name, "pos": [index*2, index*2]})

        while len(players) < MAX_PLAYERS:
            conn.send(f"Waiting for {MAX_PLAYERS - len(players)} more players...\n".encode('utf-8'))
            time.sleep(2)

        broadcast_turn_status()

        while True:
            msg = conn.recv(1024).decode('utf-8').strip().lower()
            if not msg: break

            if current_turn == index:
                if msg in ['w', 'a', 's', 'd']:
                    p_pos = players[index]["pos"]
                    if msg == 'w': p_pos[1] = (p_pos[1] - 1) % GRID_SIZE
                    if msg == 's': p_pos[1] = (p_pos[1] + 1) % GRID_SIZE
                    if msg == 'a': p_pos[0] = (p_pos[0] - 1) % GRID_SIZE
                    if msg == 'd': p_pos[0] = (p_pos[0] + 1) % GRID_SIZE
                    
                    # LOGIC: Check for Key
                    if p_pos == key_pos and not has_key:
                        has_key = True
                        broadcast(f"\n*** SYSTEM: {name} FOUND THE RUSTY KEY! ***\n")
                    
                    # LOGIC: Check for Victory
                    if p_pos == door_pos and has_key:
                        broadcast(f"\n==============================\n")
                        broadcast(f"VICTORY! {name} unlocked the door!\n")
                        broadcast(f"THE TEAM HAS ESCAPED THE ROOM!\n")
                        broadcast(f"==============================\n")
                        break # End game

                    current_turn = (current_turn + 1) % MAX_PLAYERS
                    broadcast_turn_status()
                elif msg.startswith("chat:"):
                    broadcast(f"CHAT [{name}]: {msg[5:]}")
            else:
                conn.send("WAIT: It is not your turn!\n".encode('utf-8'))
    except: pass
