# AES-256 Ransomware Behavior Simulator (ISC353 — Milestone 2)

> **This is an academic simulator built for controlled malware behavior analysis.**
> It cannot spread, persist, or cause harm outside its designated sandbox directory.
> All development was conducted under instructor supervision within an isolated VM.

---

## 🚨 **CRITICAL SAFETY NOTICE**

**⚠️ BEFORE CLONING OR RUNNING THIS CODE, READ SAFETY_NOTICE.md ⚠️**

This repository contains **functional ransomware simulation code**. While it is designed to be completely safe when run in a proper isolated environment, **improper execution could result in data loss or system compromise**.

**Do not clone this repository to:**
- Your host machine
- A production system
- Any machine containing important data
- Any networked system

**Required setup:**
- Isolated virtual machine (no network connectivity)
- VM snapshot/backup before execution
- Test data only in the sandbox directory
- Read SAFETY_NOTICE.md completely before proceeding

For detailed safety requirements, risk assessment, and usage guidelines, **consult SAFETY_NOTICE.md immediately**.

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

## Dependencies

```
cryptography>=41.0.0
```

---

## License

This project is submitted as academic coursework for **ISC 353 at Kuwait University**. It is not licensed for any use outside of this academic context. Redistribution or adaptation for non-educational purposes is prohibited.
