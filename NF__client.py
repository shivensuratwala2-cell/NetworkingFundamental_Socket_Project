import socket
import threading
import os
import winsound

# --- CONFIGURATION ---
SERVER_IP = '192.168.2.104' 
PORT = 1234

# --- AESTHETIC CONSTANTS RESTORED ---
CYAN = ""
GOLD = ""
RESET = ""
def play_background_music():
    """Final Force-Path Fix for Shivan's Snake Game"""
    try:
        import os
        # Using a raw string (r"") to prevent escape character errors
        music_file = r"C:\Users\shive\snake_game\music.wav"
        
        if os.path.exists(music_file):
            # SND_FILENAME tells Windows to look at the string as a path
            # SND_ASYNC allows the code below (SYSTEM_ADMIN) to run immediately
            winsound.PlaySound(music_file, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
            print(f"[AUDIO] SUCCESS: Playing mission audio from {music_file}")
        else:
            print(f"[AUDIO ERROR] File missing at: {music_file}")
            # This helps debug if the extension is actually music.wav.wav
            print(f"Directory Content: {os.listdir(r'C:\Users\shive\snake_game')}")
    except Exception as e:
        print(f"[AUDIO ERROR] System Failure: {e}")

def show_welcome_screen():
    """Displays a stylized monochrome entry screen with clear rules"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ASCII Art Title for better visual impact
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
    while True:
        try:
            data = sock.recv(4096).decode('utf-8')
            if not data:
                break
            # Trigger refresh on aesthetic border update
            if "╔" in data or "⚡" in data:
                print("\033[H\033[J", end="") 
            print(data)
        except:
            break

def start_client():
    show_welcome_screen()
    play_background_music()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
        while True:
            user_input = input()
            client.send(user_input.encode('utf-8'))
    except Exception as e:
        print(f"{GOLD}[FAILED] {e}{RESET}")

if __name__ == "__main__":
    start_client()
