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
    """Portable path logic: Works on any PC after downloading from GitHub"""
    try:
        import os
        # This line dynamically finds the folder where the script is RUNNING
        base_dir = os.path.dirname(os.path.abspath(__file__))
        music_file = os.path.join(base_dir, "music")
        
        if os.path.exists(music_file):
            # SND_FILENAME + SND_ASYNC ensures background playback on any Windows PC
            winsound.PlaySound(music_file, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
            print(f"[AUDIO] Protocol Initialized: Playing {os.path.basename(music_file)}")
        else:
            print(f"\n[AUDIO ERROR] music.wav not found in project folder!")
            print(f"Target Path: {music_file}")
    except Exception as e:
        print(f"[AUDIO ERROR] Hardware/Path Failure: {e}")

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
