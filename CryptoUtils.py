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
