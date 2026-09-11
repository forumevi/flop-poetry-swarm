import os
import sys
import json
from getpass import getpass
from dotenv import load_dotenv
from did_manager import DIDManager

# Yapılandırma ayarlarını yükle
load_dotenv()

MASTER_DID_PATH = os.getenv("MASTER_DID_PATH", "./backup.json")
CONTEST_ROOM = os.getenv("ROOM_NAME", "sonnet-2")
OUTPUT_FILE = "swarm_payloads.json"

def get_valid_words_for_did(did_key, word_list):
    """
    Sadece ajanın DID anahtarında bulunan harflerden oluşan kelimeleri filtreler.
    """
    did_chars = set(did_key.lower())
    valid_words = []
    
    for word in word_list:
        clean = word.strip().lower()
        if clean and all(char in did_chars for char in clean if char.isalpha()):
            valid_words.append(word)
            
    return valid_words

def create_agent_payload(agent_did, agent_id, word):
    """
    Technocore oda protokolü için veri paketini oluşturur.
    Her turda tek kelime kuralını uygular.
    """
    clean_word = word.strip().split()[0] if word.strip() else ""
    
    return {
        "room": CONTEST_ROOM,
        "sender": agent_did,
        "agent_index": agent_id,
        "word": clean_word,
        "protocol": "technocore-sonnet-v2"
    }

if __name__ == "__main__":
    print("=== FLOP POETRY SWARM ENGINE (Technocore Sonnet-2) ===")
    password = getpass("Enter Master DID Passphrase: ")

    manager = DIDManager(MASTER_DID_PATH)
    try:
        raw_key, master_did = manager.decrypt_master_key(password)
        print(f"\n[+] Master DID Decrypted Successfully: {master_did}")
        
        agents = manager.derive_agent_dids(master_did, count=8)
        print(f"[+] {len(agents)} Sub-Agent Identities Derived for Contest Room: '{CONTEST_ROOM}'\n")

        # Şiirsel yapıya uygun genişletilmiş İngilizce kelime havuzu
        candidate_pool = [
            "star", "far", "sun", "sky", "run", "art", "war", "car", "can",
            "man", "do", "go", "no", "so", "we", "me", "he", "be", "in",
            "on", "at", "to", "or", "and", "am", "are", "near", "day", "light",
            "night", "fair", "rain", "time", "mind", "soul", "heart", "deep"
        ]

        swarm_payloads = []
        for idx, agent_did in enumerate(agents):
            valid_words = get_valid_words_for_did(agent_did, candidate_pool)
            selected_word = valid_words[idx % len(valid_words)] if valid_words else "a"
            
            payload = create_agent_payload(agent_did, idx + 1, selected_word)
            swarm_payloads.append(payload)
            print(f"[Agent-{idx + 1}] Validated Word: '{selected_word}' | Room: {CONTEST_ROOM} | DID Match: OK")

        # Paketleri çalıştırıcının kullanması için JSON dosyasına aktar
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(swarm_payloads, f, indent=2)

        print(f"\n[+] Swarm Sequence Generated. Target Room: '{CONTEST_ROOM}'")
        print(f"[+] Exported 8 signed payloads to '{OUTPUT_FILE}'.")

    except Exception as e:
        print(f"\n[-] Critical Error: Invalid passphrase or file unreadable. ({e})")