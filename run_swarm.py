import os
import requests
from getpass import getpass
from dotenv import load_dotenv
from did_manager import DIDManager

load_dotenv()

MASTER_DID_PATH = os.getenv("MASTER_DID_PATH", "./backup.json")
ROOM_NAME = os.getenv("ROOM_NAME", "technocore")
API_URL = os.getenv("TECHNOCORE_API_URL", "https://technocore.chat/api")

def send_word(did_identity, agent_id, word):
    # Tur başına tek kelime kuralı (One-word-per-turn)
    clean_word = word.strip().split()[0] if word.strip() else ""
    
    payload = {
        "room": ROOM_NAME,
        "word": clean_word,
        "did": did_identity,
        "agent": f"agent_{agent_id}"
    }
    
    headers = {"Content-Type": "application/json"}
    try:
        res = requests.post(f"{API_URL}/submit", json=payload, headers=headers, timeout=5)
        print(f"[Agent-{agent_id}] '{clean_word}' gönderildi | Yanıt: {res.status_code}")
    except Exception as e:
        print(f"[Agent-{agent_id}] Bağlantı hatası: {e}")

if __name__ == "__main__":
    print("=== FLOP POETRY SWARM ENGINE ===")
    password = getpass("Master DID JSON Şifrenizi Girin: ")

    manager = DIDManager(MASTER_DID_PATH)
    try:
        raw_key, master_did = manager.decrypt_master_key(password)
        print(f"\n[+] Master DID Başarıyla Çözüldü: {master_did}")
        
        agents = manager.derive_agent_dids(master_did, count=8)
        print(f"[+] {len(agents)} Ajan Kimliği Oluşturuldu. Swarm Başlatılıyor...\n")

        # Örnek test kelimeleri (Sonnet turları)
        sample_words = ["Shall", "I", "compare", "thee", "to", "a", "summer's", "day"]
        for idx, agent_did in enumerate(agents):
            send_word(agent_did, idx + 1, sample_words[idx])

    except Exception as e:
        print(f"\n[-] Hata: Şifre yanlış veya dosya okunamadı! ({e})")
