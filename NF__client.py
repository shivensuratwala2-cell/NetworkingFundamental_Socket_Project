import socket
import threading
import os
SERVER_IP = '172.16.17.147' # Replace with actual IP
PORT = 1234


def show_welcome_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("       WELCOME TO THE TERMINAL ESCAPE ROOM")
    print("="*50)
    print("\nCONTROLS:")
    print("  W/A/S/D : Move around the 100x100 grid")
    print("  CHAT:msg : Talk to your group")
    print("\nRULES:")
    print("1. Find the hidden Key first.")
    print("2. Navigate to the Door (D) to escape.")
    print("3. You can only move on 'YOUR TURN'.")
    print("="*50)
    input("\nPress ENTER to connect...")

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096).decode('utf-8')
            if data:
                print(data)
        except:
            print("\n[DISCONNECTED FROM SERVER]")
            break

def start_client():
    show_welcome_screen()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[CONNECTING] Attempting to reach {SERVER_IP}...")
    
    try:
        client.connect((SERVER_IP, PORT))
        print("[SUCCESS] Connection established!")
    except Exception as e:
        print(f"[FAILED] Connection error: {e}")
        return

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        cmd = input()
        client.send(cmd.encode('utf-8'))

if __name__ == "__main__":
    start_client()
