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
