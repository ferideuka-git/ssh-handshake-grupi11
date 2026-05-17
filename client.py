import socket
import json
import logging
import os
from crypto_utils import *

HOST = "127.0.0.1"
PORT = 2222
KNOWN_HOSTS = "known_hosts.txt"

logging.basicConfig(level=logging.INFO, format='[CLIENT] %(asctime)s - %(levelname)s - %(message)s')

def save_host(pubkey):
    with open(KNOWN_HOSTS, "w") as f:
        f.write(pubkey)

def load_host():
    if not os.path.exists(KNOWN_HOSTS):
        return None
    with open(KNOWN_HOSTS, "r") as f:
        return f.read()

def main():
    print("="*50)
    print("Welcome to Simplified SSH Client.")
    print("="*50)
    print("Attempting to connect to the SSH server...")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("Starting handshake protocol...")

        # 1. Algorithm Negotiation
        logging.info("Step 1: Sending algorithm preferences...")
        proposal = {
            "kex": ["x25519"],
            "encryption": ["AES256"],
            "hmac": ["SHA256"]
        }
        client.send(json.dumps(proposal).encode('utf-8'))
        
        chosen = json.loads(client.recv(4096).decode('utf-8'))
        logging.info(f"Negotiated algorithms: {chosen}")

        # 2. Key Exchange (Diffie-Hellman)
        logging.info("Step 2: Exchanging Diffie-Hellman keys...")
        client_dh_priv, client_dh_pub = generate_dh_keypair()
        
        client.send(client_dh_pub.public_bytes_raw())
        server_dh_pub_bytes = client.recv(4096)
        
        shared_key = derive_shared_key(client_dh_priv, server_dh_pub_bytes)
        logging.info("Shared master secret derived successfully.")

        # 3. Server Authentication & MITM Protection
        logging.info("Step 3: Verifying server identity...")
        auth_payload = json.loads(client.recv(4096).decode('utf-8'))
        
        server_public_key_pem = auth_payload["public_key"]
        signature = bytes.fromhex(auth_payload["signature"])

        # Kontrolli i MITM (Man-in-the-Middle) përmes known_hosts
        known_key = load_host()
        if known_key and known_key != server_public_key_pem:
            print("\n" + "!"*50)
            print("WARNING: POSSIBLE MAN-IN-THE-MIDDLE ATTACK!")
            print("Server host key has changed!")
            print("!"*50 + "\n")
            return
        elif not known_key:
            logging.info("New host. Saving server public key to known_hosts.txt")
            save_host(server_public_key_pem)

        # Verifikimi i nënshkrimit digjital të serverit
        if verify_signature(server_public_key_pem.encode('utf-8'), signature, shared_key):
            print("Server identity verified. Handshake successful.")
        else:
            logging.error("Verification failed! Server signature is invalid.")
            return

        # 4. Secure Channel & Message Sending
        logging.info("Step 4: Setting up secure symmetric channel...")
        iv = client.recv(16)
        
        message = b"Hello secure server! This is a confidential SSH session."
        encrypted_msg = aes_encrypt(shared_key, message, iv)
        mac = create_hmac(shared_key, encrypted_msg)

        # Dërgimi i të dhënave si strukturë e pastër JSON për të shmangur gabimet e TCP
        secure_package = {
            "encrypted": encrypted_msg.hex(),
            "mac": mac.hex()
        }
        client.send(json.dumps(secure_package).encode('utf-8'))
        
        print("\n" + "="*50)
        print("Secure channel established. You can now begin your session.")
        print("Secure message sent to server.")
        print("="*50 + "\n")

    except Exception as e:
        logging.error(f"Connection or Handshake error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()