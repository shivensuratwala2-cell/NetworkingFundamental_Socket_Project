import socket
import threading
import os

# --- CONFIGURATION ---
SERVER_IP = '192.168.1.41' 
PORT = 1234

# --- AESTHETIC CONSTANTS ---
# Kept as empty strings for the monochrome look you requested
CYAN = ""
GOLD = ""
RESET = ""

def show_welcome_screen():
    """Displays a stylized monochrome entry screen with clear rules"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ASCII Art Title for visual impact
    title_art = r"""
    ############################################################
    #     _____   _____   _____   _____   _____   _____        #
    #    |   __| |   __| |     | |  _  | |  _  | |   __|       #
    #    |   __| |__   | |   --| |     | |   __| |   __|       #
    #    |_____| |_____| |_____| |__|__| |__|    |_____|       #
    #                                                          #
    #                TERMINAL ESCAPE ROOM                      #
    ############################################################
    """
    print(title_art)
    
    print("\n" + "="*60)
    print(f"{'MISSION PARAMETERS & REGULATIONS':^60}")
    print("="*60)
    
    print(f" 1. OBJECTIVE   : Locate the encrypted Data Key (K) on the grid.")
    print(f" 2. EXTRACTION  : After securing (K), the Exit Door (D) appears.")
    print(f" 3. CO-OP MODE  : Turn-based movement. Coordinate via Comms.")
    print(f" 4. PERFORMANCE : Efficiency is tracked by 'Play Time' (MM:SS).")
    
    print("\n" + "-"*60)
    print(f"{'OPERATIONAL CONTROLS':^60}")
    print("-"*60)
    
    print(f" [MOVEMENT]     : Use 'W', 'A', 'S', 'D' + [ENTER] to move.")
    print(f" [COMMS]        : Type 'chat:<message>' to talk to agents.")
    print(f" [TERMINATE]    : Type 'exit' to disconnect from the hub.")
    
    print("\n" + "="*60)
    print(f"{'STRICT ADHERENCE TO PROTOCOL IS MANDATORY':^60}")
    print("="*60)
    
    input("\n >>> PRESS [ENTER] TO INITIALIZE NEURAL LINK... ")

def receive_messages(sock):
    """Handles incoming map updates and chat from the server"""
    while True:
        try:
            data = sock.recv(4096).decode('utf-8')
            if not data:
                break
            # Trigger refresh (ANSI Clear) on aesthetic border update
            if "╔" in data or "⚡" in data:
                print("\033[H\033[J", end="") 
            print(data)
        except:
            break

def start_client():
    """Initializes the socket connection and threading"""
    show_welcome_screen()
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\n[CONNECTING] Pinging mission hub at {SERVER_IP}...")
    
    try:
        client.connect((SERVER_IP, PORT))
        print(f"[SUCCESS] Connection established!")
        
        # Start background thread for real-time updates
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
        
        while True:
            user_input = input()
            if user_input.lower() == 'exit':
                break
            client.send(user_input.encode('utf-8'))
            
    except Exception as e:
        print(f"[FAILED] Could not reach the server: {e}")

if __name__ == "__main__":
    start_client()
