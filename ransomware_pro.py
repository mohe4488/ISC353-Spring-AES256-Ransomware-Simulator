import os
import json
import time
import math
import hashlib
from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# --- WARNING: FOR EDUCATIONAL USE ONLY ---
print("====================================================")
print("⚠️  SIMULATOR ONLY — DO NOT RUN OUTSIDE VM ⚠️")
print("====================================================")

TARGET_DIR = "/sandbox/test_files/"
KEY_PATH = "/sandbox/secret.key"
LOG_PATH = "/sandbox/logs/behavior_log.json"

def calculate_entropy(data):
    if not data: return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def get_sha256(data):
    return hashlib.sha256(data).hexdigest()

def log_behavior(event_type, file_info):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": file_info
    }
  
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def get_key():
    if not os.path.exists(KEY_PATH):
        key = AESGCM.generate_key(bit_length=256)
        with open(KEY_PATH, "wb") as f: f.write(key)
        return key
    with open(KEY_PATH, "rb") as f: return f.read()

def encrypt_files():
    aesgcm = AESGCM(get_key())
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".locked") or filename == "secret.key": continue
        path = os.path.join(TARGET_DIR, filename)
        with open(path, "rb") as f: data = f.read()
        
        start_time = time.time()
        nonce = os.urandom(12) 
        encrypted_data = aesgcm.encrypt(nonce, data, None)
        
        with open(path + ".locked", "wb") as f: f.write(nonce + encrypted_data)
        
        log_behavior("ENCRYPTION", {
            "file": filename,
            "orig_sha256": get_sha256(data),
            "orig_entropy": calculate_entropy(data),
            "enc_entropy": calculate_entropy(encrypted_data),
            "duration": time.time() - start_time
        })
        os.remove(path)
        print(f"[+] Encrypted: {filename}")

def decrypt_files():
    aesgcm = AESGCM(get_key())
    for filename in os.listdir(TARGET_DIR):
        if not filename.endswith(".locked"): continue
        path = os.path.join(TARGET_DIR, filename)
        with open(path, "rb") as f: 
            raw_data = f.read()
            nonce = raw_data[:12]
            encrypted_content = raw_data[12:]
        
        decrypted_data = aesgcm.decrypt(nonce, encrypted_content, None)
        original_path = path.replace(".locked", "")
        with open(original_path, "wb") as f: f.write(decrypted_data)
        
        log_behavior("DECRYPTION", {
            "file": original_path,
            "restored_sha256": get_sha256(decrypted_data)
        })
        os.remove(path)
        print(f"[-] Decrypted: {original_path}")

if __name__ == "__main__":
    choice = input("Enter 'E' to Encrypt or 'D' to Decrypt: ").upper()
    if choice == 'E': encrypt_files()
    elif choice == 'D': decrypt_files()
    else: print("Invalid Choice.")

