import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class DIDManager:
    def __init__(self, json_path):
        self.json_path = json_path

    def decrypt_master_key(self, password):
        with open(self.json_path, "r", encoding="utf-8") as f:
            backup = json.load(f)

        salt = base64.urlsafe_b64decode(backup["salt"] + "==")
        iv = base64.urlsafe_b64decode(backup["iv"] + "==")
        ciphertext = base64.urlsafe_b64decode(backup["data"] + "==")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=250000,
        )
        key = kdf.derive(password.encode())
        aesgcm = AESGCM(key)
        
        decrypted_bytes = aesgcm.decrypt(iv, ciphertext, None)
        return decrypted_bytes.decode("utf-8"), backup["did"]

    def derive_agent_dids(self, master_did, count=8):
        # Master DID üzerinden 8 alt otonom ajan kimliği türetme
        return [f"{master_did}#agent-{i}" for i in range(1, count + 1)]
