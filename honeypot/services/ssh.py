import logging.config
import socket
import threading
import logging

logging.basicConfig(filename="ssh_honeypot.log", level=logging.INFO)

BANNER = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n"

def handle_client(client_socket, addr):
    logging.info(f"[+] Connection from {addr}")
    client_socket.send(BANNER)
    data = client_socket.recv(1024)
    logging.info(f"[SSH] Received from {addr}: {data.decode(errors='ignore').strip()}")
    client_socket.close()

def start_ssh_honeypot(host='0.0.0.0', port=22):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    # this means that it listens for up to 5 connections, blocking anything beyond that
    sock.listen(5) 
    print(f"[SSH Honeypot] Listening on {host}:{port}")

    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_client, args=(client,addr)).start()

if __name__ == "__main__":
    start_ssh_honeypot()
