from cryptography.hazmat.primitives.asymmetric import rsa, padding, x25519
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidSignature
import os, hmac, hashlib

# ================= RSA (Server Authentication) =================
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
     public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_pem


def sign_data(private_key, data):
    return private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
def verify_signature(public_pem, signature, data):
    try:
        public_key = serialization.load_pem_public_key(public_pem)
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
       except InvalidSignature:
        return False



    # ================= Diffie-Hellman (X25519) =================
def generate_dh_keypair():
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_key(private_key, peer_public_bytes):
    peer_public = x25519.X25519PublicKey.from_public_bytes(peer_public_bytes)
    return private_key.exchange(peer_public)

# ================= AES-256 CFB Enkriptimi =================
def aes_encrypt(key, plaintext, iv):
    cipher = Cipher(algorithms.AES(key[:32]), modes.CFB(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()

def aes_decrypt(key, ciphertext, iv):
    cipher = Cipher(algorithms.AES(key[:32]), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# ================= HMAC SHA256 =================
def create_hmac(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()

def verify_hmac(key, data, mac):
    return hmac.compare_digest(create_hmac(key, data), mac)