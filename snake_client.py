import socket
import threading

# Replace with the Server PC's IPv4 address
SERVER_IP = '192.168.2.105' 
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

def receive_messages():
    while True:
        try:
            print("\n" + client.recv(1024).decode('utf-8'))
        except:
            print("Disconnected.")
            break

# Thread to listen for other players' moves/chats while you type
threading.Thread(target=receive_messages, daemon=True).start()

print("CONTROLS: w/a/s/d to move. Type 'CHAT:message' to talk.")
while True:
    cmd = input("Enter command: ")
    client.send(cmd.encode('utf-8'))

def draw_grid(player_positions):
    # Create a 10x10 empty grid
    grid_size = 10
    grid = [[" . " for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Place players on the grid
    for addr, pos in player_positions.items():
        x, y = pos[0], pos[1]
        # Keep within bounds
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y][x] = " S " # 'S' represents a Snake piece
            
    # Clear terminal and print
    print("\n" * 20) # Simple way to 'clear' the CLI
    for row in grid:
        print("".join(row))
    print("\nControls: w/a/s/d | Chat: CHAT:message")

import socket
import threading

# ... existing connection code ...
name = input("Enter your name: ") # Capture name before starting

def receive_messages():
    while True:
        try:
            # When a message is received, it will now contain the sender's name
            print(client.recv(1024).decode('utf-8'))
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

while True:
    cmd = input(f"{name}> ")
    # Format the message to include the name so the server knows who sent it
    full_message = f"NAME:{name}|CMD:{cmd}"
    client.send(full_message.encode('utf-8'))
