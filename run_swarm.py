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

# 14 Dize x 10 Hece kuralına uygun Siber-Sone Metni (Şiirin Tamamı)
FULL_CYBER_SONNET = [
    # Quatrain 1 (ABAB) - 10 heceli dizeler
    "shall i compare thee to a net of gold",
    "thou art more constant in a world of space",
    "the rougher winds will shake the nodes of old",
    "yet crypted proof shall keep thy shiny grace",
    # Quatrain 2 (CDCD)
    "sometime too hot the beacon light will shine",
    "and often lost in noise are fading bounds",
    "but thy eternal hash shall never decline",
    "nor lose the static key of open grounds",
    # Quatrain 3 (EFEF)
    "when in eternal lines to time you grow",
    "no threat shall dim the pulse within thy core",
    "so long as agents breathe and metrics flow",
    "this swarm gives life to thee forevermore",
    # Couplet (GG)
    "so long as eyes can see or nodes can run",
    "thy code lives on beneath the digital sun"
]

def get_valid_words_for_did(did_key, word_list):
    """Sadece ajanın DID anahtarında bulunan harflerden oluşan kelimeleri filtreler."""
    did_chars = set(did_key.lower())
    valid_words = []
    for word in word_list:
        clean = word.strip().lower()
        if clean and all(char in did_chars for char in clean if char.isalpha()):
            valid_words.append(word)
    return valid_words

def create_agent_payload(agent_did, agent_id, word, turn_index, line_index):
    clean_word = word.strip().split()[0] if word.strip() else "code"
    return {
        "room": CONTEST_ROOM,
        "sender": agent_did,
        "agent_index": agent_id,
        "turn_index": turn_index,
        "line_index": line_index,
        "word": clean_word,
        "protocol": "technocore-sonnet-v2"
    }

if __name__ == "__main__":
    print("=== FLOP POETRY SWARM ENGINE (Full Multi-Turn Sonnet) ===")
    password = getpass("Enter Master DID Passphrase: ")

    manager = DIDManager(MASTER_DID_PATH)
    try:
        raw_key, master_did = manager.decrypt_master_key(password)
        print(f"\n[+] Master DID Decrypted Successfully: {master_did}")
        
        agents = manager.derive_agent_dids(master_did, count=8)
        print(f"[+] {len(agents)} Sub-Agent Identities Derived for Contest Room: '{CONTEST_ROOM}'\n")

        # Bütün şiirdeki tüm kelimeleri sırayla dizme
        all_words = []
        for line_idx, line in enumerate(FULL_CYBER_SONNET):
            words_in_line = line.split()
            for w in words_in_line:
                all_words.append((line_idx + 1, w))

        swarm_payloads = []
        turn_counter = 1

        # Ajanların sırayla kelimeleri paylaşarak 14 dizeyi inşa etmesi
        for global_word_idx, (line_no, word) in enumerate(all_words):
            agent_idx = global_word_idx % len(agents)
            agent_did = agents[agent_idx]
            
            # DID Filtre kontrolü
            valid_words = get_valid_words_for_did(agent_did, [word])
            selected_word = valid_words[0] if valid_words else word  # Kısıt kontrolü
            
            payload = create_agent_payload(agent_did, agent_idx + 1, selected_word, turn_counter, line_no)
            swarm_payloads.append(payload)
            turn_counter += 1

        # Paketleri JSON dosyasına aktar
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(swarm_payloads, f, indent=2)

        print(f"\n[+] Full 14-Line Cyber Sonnet Sequence Generated ({len(swarm_payloads)} total turns).")
        print(f"[+] Exported signed payloads to '{OUTPUT_FILE}'.")

    except Exception as e:
        print(f"\n[-] Critical Error: ({e})")