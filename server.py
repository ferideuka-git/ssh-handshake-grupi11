import os
import json
import logging
from crypto_utils import *

HOST = "127.0.0.1"
PORT = 2222

logging.basicConfig(level=logging.INFO, format='[SERVER] %(asctime)s - %(levelname)s - %(message)s')

def main():
    print("="*50)
    print("Server starting up...")
    print("="*50)
    
    # Gjenerimi i Host Keys të Serverit (Simulim i databazës së serverit)
    server_private_rsa, server_public_pem = generate_rsa_keys()
    logging.info("RSA Host Keys generated successfully.")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print("Awaiting client connections...")
    conn, addr = server.accept()
    print(f"Client connected! Initiating handshake with {addr}...")

    try:
        # 1. Algorithm Negotiation
        logging.info("Step 1: Negotiating algorithms...")
        client_proposal = json.loads(conn.recv(4096).decode('utf-8'))
        logging.info(f"Received client proposal: {client_proposal}")
        
        chosen_algorithms = {
            "kex": "x25519",
            "encryption": "AES256",
            "hmac": "SHA256"
        }
        conn.send(json.dumps(chosen_algorithms).encode('utf-8'))
        logging.info(f"Sent negotiated algorithms: {chosen_algorithms}")

        # 2. Key Exchange (Diffie-Hellman)
        logging.info("Step 2: Performing Diffie-Hellman Key Exchange...")
        server_dh_priv, server_dh_pub = generate_dh_keypair()
        
        client_dh_pub_bytes = conn.recv(4096)
        conn.send(server_dh_pub.public_bytes_raw())
        
        shared_key = derive_shared_key(server_dh_priv, client_dh_pub_bytes)
        logging.info("Shared master secret derived successfully.")

        # 3. Server Authentication (Digital Signature)
        logging.info("Step 3: Authenticating server identity...")
        # Nënshkruhet 'shared_key' për të vërtetuar zotërimin e tij dhe identitetin e serverit
        signature = sign_data(server_private_rsa, shared_key)
        
        auth_payload = {
            "public_key": server_public_pem.decode('utf-8'),
            "signature": signature.hex()
        }
        conn.send(json.dumps(auth_payload).encode('utf-8'))
        logging.info("Sent Host Public Key and Digital Signature to client.")

        # 4. Secure Channel Activation
        logging.info("Step 4: Activating Encrypted Channel...")
        iv = os.urandom(16)
        conn.send(iv) # Dërgohet IV për AES
        
        # Pranohet paketa e enkriptuar (përdorim JSON që të mos kemi përzierje të TCP)
        secure_package = json.loads(conn.recv(4096).decode('utf-8'))
        encrypted_msg = bytes.fromhex(secure_package["encrypted"])
        received_mac = bytes.fromhex(secure_package["mac"])
        
        # Verifikimi i Integritetit (HMAC)
        if verify_hmac(shared_key, encrypted_msg, received_mac):
            logging.info("HMAC Verification: SUCCESS. Data integrity verified.")
            decrypted_msg = aes_decrypt(shared_key, encrypted_msg, iv)
            
            print("\n" + "="*50)
            print("Handshake successful. Proceeding to establish secure channel...")
            print(f"Received secure message: {decrypted_msg.decode('utf-8')}")
            print("="*50 + "\n")
        else:
            logging.error("HMAC verification failed! Message might be tampered.")

    except Exception as e:
        logging.error(f"Handshake failed due to error: {e}")
    finally:
        conn.close()
        server.close()
        print("Session closed.")

if __name__ == "__main__":
    main()