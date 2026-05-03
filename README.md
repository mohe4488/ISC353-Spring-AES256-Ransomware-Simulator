# AES-256 Ransomware Behavior Simulator (ISC353 — Milestone 2)

> **This is an academic simulator built for controlled malware behavior analysis.**
> It cannot spread, persist, or cause harm outside its designated sandbox directory.
> All development was conducted under instructor supervision within an isolated VM.

---

## Team Members

1- Abdelrahman Elshabrawi 
2- Mohyaldeen Osman

**Kuwait University · College of Life Sciences · Department of Information Science**
**Course:** ISC 353 · **Project Phase:** Milestone 2 — Core Build

---

## ⚠️ Safety Statement

This simulator was designed from the ground up to be **safe, controlled, and fully reversible**. The following constraints are hard-coded and verified:

| Safety Guarantee | How It Is Enforced |
|---|---|
| **Scope-limited** | Targets only `./sandbox/test_files/` — enforced by the `TARGET_DIR` constant at the top of the script |
| **No network activity** | Zero network imports or socket calls anywhere in the codebase |
| **No persistence** | No registry edits, no cron jobs, no startup entries, no system modifications |
| **No self-propagation** | No directory traversal beyond `TARGET_DIR`; no process spawning |
| **Fully reversible** | `decrypt_files()` restores originals byte-for-byte, verified by SHA-256 hash matching |
| **Isolated execution** | Runs only inside a Kali Linux VM with no host network access |
| **Instructor pre-approved** | Code was reviewed by the course instructor before the first execution (Milestone 1 evidence on file) |

---

## What This Simulator Does

The simulator is a **modular Python application** that replicates the core cryptographic behavior of ransomware in a completely safe, sandboxed environment. It serves two purposes:

1. **Simulate** the encryption/decryption lifecycle of a ransomware attack using AES-256-GCM.
2. **Generate Ground Truth telemetry** — behavioral fingerprints (entropy, hashes, timing) that will feed YARA detection rules in Milestone 3.

### Architecture

The codebase is organized around three pillars:

```
ransomware_pro.py
│
├── Cryptographic Core       → get_key(), encrypt_files(), decrypt_files()
├── Behavioral Metric Engine → calculate_entropy(), get_sha256()
└── Forensic Logger          → log_behavior() → sandbox/logs/behavior_log.json
```

---

## Project Structure

```
project-root/
│
├── ransomware_pro.py              # Main simulator script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
└── sandbox/                       # Isolated working environment (VM only)
    ├── test_files/                # Target directory — only files here are touched
    │   ├── sample.txt
    │   ├── sample.txt.locked      # Created after encryption
    │   └── ...
    ├── secret.key                 # AES-256 key (auto-generated, stays in sandbox)
    └── logs/
        └── behavior_log.json      # Structured telemetry output
```

---

## How to Run

> **Prerequisites:** Python 3.8+, running inside an isolated VM. Do not run on a host machine.

### 1. Install Dependencies

```bash
pip install cryptography
```

Or if a `requirements.txt` is present:

```bash
pip install -r requirements.txt
```

### 2. Prepare the Sandbox

Ensure the target directory exists and contains test files:

```bash
mkdir -p sandbox/test_files sandbox/logs
cp your_test_files/* sandbox/test_files/
```

### 3. Run the Simulator

```bash
python ransomware_pro.py
```

You will be prompted:

```
Enter 'E' to Encrypt or 'D' to Decrypt:
```

- Press **`E`** → encrypts all files in `sandbox/test_files/`, appending `.locked` to each
- Press **`D`** → decrypts all `.locked` files and restores originals

### 4. Inspect the Telemetry

```bash
cat sandbox/logs/behavior_log.json
```

Each line is a JSON entry capturing the behavioral fingerprint of one file operation.

---

## Technical Implementation

### Cryptographic Core — AES-256-GCM

The simulator uses **AES-256 in Galois/Counter Mode (GCM)** for authenticated encryption, sourced from Python's `cryptography.hazmat` library.

**Key generation** — a 256-bit cryptographically secure key is generated once and stored:
```python
def get_key():
    if not os.path.exists(KEY_PATH):
        key = AESGCM.generate_key(bit_length=256)
        with open(KEY_PATH, "wb") as f: f.write(key)
        return key
    with open(KEY_PATH, "rb") as f: return f.read()
```

**Encryption** — a unique 12-byte nonce is generated per file and prepended to the ciphertext:
```python
nonce = os.urandom(12)
encrypted_data = aesgcm.encrypt(nonce, data, None)
with open(path + ".locked", "wb") as f:
    f.write(nonce + encrypted_data)
```

**Decryption** — the nonce is recovered from the first 12 bytes to enable authenticated decryption:
```python
nonce = raw_data[:12]
encrypted_content = raw_data[12:]
decrypted_data = aesgcm.decrypt(nonce, encrypted_content, None)
```

GCM mode was selected because it includes a built-in **authentication tag** that verifies ciphertext integrity, preventing silent data corruption during recovery.

---

### Behavioral Metric Engine

Beyond encryption, the simulator fingerprints each operation using two statistical measures:

**Shannon Entropy** — measures the randomness of file data before and after encryption:
```python
def calculate_entropy(data):
    if not data: return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy
```

**SHA-256 Integrity Fingerprint** — generates hash digests for pre/post comparison:
```python
def get_sha256(data):
    return hashlib.sha256(data).hexdigest()
```

---

### Forensic Logging

All activity is written to `sandbox/logs/behavior_log.json` in newline-delimited JSON:

```python
def log_behavior(event_type, file_info):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": file_info
    }
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

**Example log entry (ENCRYPTION):**
```json
{
  "timestamp": "2025-06-01T14:23:11.482103",
  "event": "ENCRYPTION",
  "details": {
    "file": "project.txt",
    "orig_sha256": "e529...8a114",
    "orig_entropy": 4.32,
    "enc_entropy": 5.95,
    "duration": 0.0007
  }
}
```

---

## Behavioral Signals (Feeds Milestone 3 YARA Detection)

The telemetry captured by this simulator will be used to calibrate YARA detection rules in Milestone 3. The key signals are:

| Signal | Observation | Detection Implication |
|---|---|---|
| **Entropy delta** | Text files: ~4.5 → ~7.99 after encryption | Large Δentropy in rapid succession = encryption event |
| **JPG entropy** | ~7.91 → ~7.95 (near-static) | Pre-compressed files are poor encryption indicators |
| **Execution time** | ~0.001–0.09s per file | Burst of fast file operations = ransomware-like activity |
| **File rename** | Original removed, `.locked` version appears | Atomic rename/replace is a known ransomware signature |
| **SHA-256 match** | Hash before = hash after full cycle | Confirms 100% integrity restoration |

### Entropy Results by File Type

| File | Original Entropy | Encrypted Entropy | Δ Entropy | Time (s) |
|---|---|---|---|---|
| project.txt | 4.32 | 5.95 | +1.63 | 0.0007 |
| data.docx | 4.45 | 5.89 | +1.44 | 0.0008 |
| lab_report.pdf | 4.14 | 5.82 | +1.68 | 0.0013 |
| photo1.jpg | 7.91 | 7.95 | +0.04 | 0.0123 |
| schedule.xlsx | 4.74 | 6.24 | +1.50 | 0.0924 |

> **Key finding:** Structured text files show a significant entropy jump (~+1.5), while pre-compressed formats (JPG) remain nearly flat. This distinction informs the entropy threshold selection for YARA rules.

---

## Week 3 Plan

- **YARA Rule Development:** Design and test detection rules based on entropy thresholds and `.locked` rename signatures identified in this milestone.
- **3-2-1 Backup Strategy Demo:** Demonstrate full data recovery from a simulated ransomware incident using the 3-2-1 backup model.
- **Final Report:** Consolidate all milestones into a complete academic submission.

---

## Dependencies

```
cryptography>=41.0.0
```

---

## AI Usage Disclosure

In accordance with academic integrity guidelines, **Google Gemini** was used during Milestone 2 for:

- Code optimization toward the AES-256-GCM standard using `cryptography.hazmat`
- Technical report drafting and academic terminology guidance
- Debugging the JSON logging and Shannon Entropy calculation

All AI-assisted code was manually reviewed, tested, and executed by the team. All SHA-256 verifications and forensic data interpretations were performed independently.

---

## License

This project is submitted as academic coursework for **ISC 353 at Kuwait University**. It is not licensed for any use outside of this academic context. Redistribution or adaptation for non-educational purposes is not permitted.
