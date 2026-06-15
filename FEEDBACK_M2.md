# M2 Pregrade — Instructor Feedback

**Pair 2** — Abdelrahman Elshabrawi & Mohyaldeen Osman
**Assigned project:** Project 4 — Ransomware Behavior Analysis & Defense
**Reviewed commit:** `cc2af5b` on `main`
**Reviewed on:** 2026-05-03 (Sunday, the day of the M2 deadline)
**Reviewer:** Dr. Shaikhah Alkhadhr (sole grader, ISC353)

---

> **What this document is.** This is a **pregrade** — a formative review of your repository state ahead of the official M2 grading on **Tuesday, 2026-05-05** (two days after the M2 deadline). It is *not* your final mark. Treat the scores below as advisory: they show you exactly where the rubric currently lands based on what's in your repo today, and where the easiest points are still on the table. You have a short window to act on this feedback before the summative grade is locked in.
>
> The official M2 grade will be computed against **the full Moodle submission** (PDF report + GitHub repo + demo video). Several rubric rows below are scored as `0` *in this pregrade* simply because they live in the PDF/video, not the repo — they will be re-scored fairly from your full submission.

---

## A note before the score table

Two things stood out when I opened the repo, and I want to surface them up front so the score table makes sense:

1. **The committed `ransomware_pro.py` is a *fragment*.** The file starts at line 1 with an indented statement (`path = os.path.join(TARGET_DIR, filename)`) — meaning everything *above* that line in your local copy is missing from the commit. There are no `import` statements, no `def encrypt_files():` opening, no helper definitions for `log_behavior`, `get_sha256`, `calculate_entropy`, `get_key`, and no `TARGET_DIR` constant. As committed, the file will raise `NameError` on the first reference and won't run at all. I'm fairly sure your local copy is complete and only the upload was truncated — but the rubric scores what's in the repo, so this is the single most impactful thing to fix today.

2. **Only one author appears in the commit history.** The single commit on `main` is by `mohe4488` (Mohyaldeen) and was made via the GitHub web UI ("Create ransomware_pro.py"). I'm **not** treating this as a partner-work deduction in the pregrade — but for the official grade I'll need to see Abdelrahman Elshabrawi's involvement reflected somewhere (commits from his account, or a clear written split in the PDF).

---

## Pregrade score table (repo-only)

| Rubric row | Max | Pregrade | Notes |
|---|---:|---:|---|
| Technical Correctness | 30 | **5 / 30** | The *design* is genuinely good (see "What's working well") but the committed file is a fragment that won't execute. With the missing pieces re-uploaded, this row could move substantially before Tuesday. |
| Code Quality | 15 | **2 / 15** | Single web-UI commit, no README, no `requirements.txt`, no `.gitignore`, no `/sandbox/test_files/` directory or sample target files, no commit-message narrative. |
| Results & Evidence | 15 | **0 / 15** | *Will be re-scored from full submission* (behavioral fingerprinting log samples, entropy plots, encryption-duration tables in PDF). |
| Technical Writing | 15 | **0 / 15** | *Will be re-scored from full submission* (PDF report). |
| Demo Video | 10 | **0 / 10** | *Will be re-scored from full submission* (3–5 min demo video). |
| Challenges Reflection | 5 | **0 / 5** | *Will be re-scored from full submission* (PDF). |
| Week 3 Plan & AI Disclosure | 10 | **0 / 10** | *Will be re-scored from full submission* (PDF). |
| **Pregrade total** | **100** | **7 / 100** | The 55 marks tied to PDF + video are recoverable on Tuesday. Critically, the 30-mark Technical Correctness row is mostly recoverable just by **re-uploading the complete file** — the design work is already done. |

---

## What's working well

I want to be clear: from what's visible in the fragment, your **design instincts on this project are strong**. Several of these choices show real maturity for an undergraduate security course, and they are exactly the things I look for in a P4 submission:

- **You picked AES-GCM, not AES-CBC.** Most students reach for `AES.MODE_CBC` (or worse, ECB) and miss the integrity check. AES-GCM gives you authenticated encryption out of the box — meaning a defender can't tamper with the ciphertext and have it silently decrypt to garbage. This is the right primitive for a ransomware simulator.
- **Fresh 12-byte nonce per file.** `os.urandom(12)` per encryption call is exactly correct for GCM (96-bit nonce is the recommended size). You also prepend the nonce to the ciphertext on disk and parse it back out on decrypt — that's the standard pattern, and you got it right.
- **Reversibility is preserved.** The brief is explicit that the simulator must be reversible; your `decrypt_files()` reads the nonce prefix, decrypts with the same key, and writes the original file back. Without this the entire submission would be invalid for safety reasons — and you have it.
- **Behavioral fingerprinting is well-thought-out.** Logging *original SHA-256, original entropy, encrypted entropy, and duration* per file is a very nice telemetry choice. Entropy delta in particular is the textbook signal that real EDR/YARA rules use to flag encryption events — so this directly sets up your M3 detection work.
- **Scope discipline is visible.** The encrypt loop targets `TARGET_DIR` only, not the whole filesystem; there's no networking, no persistence mechanism, no registry tampering, no spread/worm logic. That matches the strict P4 safety rules.

If the missing top of the file is comparable in quality to what's visible, this is one of the more thoughtful designs in the cohort. The gap is pure mechanical (incomplete upload), not conceptual.

---

## Suggestions to strengthen things before official grading

### Suggestion 1 — Re-upload the complete file (highest leverage, takes 5 minutes)

Push the complete `ransomware_pro.py` from your local copy. As reference, here's a runnable skeleton that matches the fragment you committed — use it as a sanity-check against your local version, not as a replacement:

```python
import os, time, json, math, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

TARGET_DIR = "./sandbox/test_files"          # NEVER set this to a real path
KEY_FILE   = "./sandbox/key.bin"             # generated once, kept inside sandbox
LOG_FILE   = "./sandbox/behavior_log.jsonl"  # one JSON object per line

def get_key() -> bytes:
    if not os.path.exists(KEY_FILE):
        key = AESGCM.generate_key(bit_length=256)  # AES-256 per the brief
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        with open(KEY_FILE, "wb") as f: f.write(key)
        return key
    with open(KEY_FILE, "rb") as f: return f.read()

def get_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def calculate_entropy(data: bytes) -> float:
    if not data: return 0.0
    counts = [0] * 256
    for b in data: counts[b] += 1
    total = len(data)
    return -sum((c/total) * math.log2(c/total) for c in counts if c)

def log_behavior(event_type: str, payload: dict) -> None:
    payload = {"event": event_type, "ts": time.time(), **payload}
    with open(LOG_FILE, "a") as f: f.write(json.dumps(payload) + "\n")

def encrypt_files():
    aesgcm = AESGCM(get_key())
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".locked"): continue   # skip already-encrypted
        # ... (your existing inner block: read, nonce, encrypt, write .locked, log, remove original)

def decrypt_files():
    # ... (your existing decrypt loop)

if __name__ == "__main__":
    os.makedirs(TARGET_DIR, exist_ok=True)
    choice = input("Enter 'E' to Encrypt or 'D' to Decrypt: ").upper()
    if   choice == 'E': encrypt_files()
    elif choice == 'D': decrypt_files()
    else: print("Invalid Choice.")
```

The key things to verify in your local copy before re-uploading:

- All imports are present (`os`, `time`, `json`, `math`, `hashlib`, `AESGCM` from `cryptography`).
- `TARGET_DIR` is defined and points to `./sandbox/test_files` (not a real path).
- `get_key()`, `log_behavior()`, `get_sha256()`, `calculate_entropy()` are all defined.
- `aesgcm = AESGCM(get_key())` appears at the top of `encrypt_files()` (it's currently shown only inside `decrypt_files`).
- The outer `for filename in os.listdir(TARGET_DIR):` loop in `encrypt_files()` is included.

### Suggestion 2 — Commit a `sandbox/test_files/` directory with sample targets

The whole point of the sandbox constraint is that the simulator only ever touches files inside it. Make that visible in the repo:

```
sandbox/
├── test_files/
│   ├── doc1.txt        # "lorem ipsum" content — generated, never anything personal
│   ├── doc2.txt
│   └── image1.bin      # random bytes; demonstrates entropy delta is meaningful
├── behavior_log.jsonl  # output of a clean encrypt+decrypt run
└── README.md           # one paragraph: "this is the only directory the simulator touches"
```

Generating sample files in one line:

```bash
mkdir -p sandbox/test_files && \
  for i in 1 2 3; do echo "lorem ipsum $i" > sandbox/test_files/doc$i.txt; done && \
  head -c 1024 /dev/urandom > sandbox/test_files/random1.bin
```

Then run encrypt + decrypt once and commit `sandbox/behavior_log.jsonl` as evidence (Results & Evidence row).

### Suggestion 3 — Add a `README.md` covering the safety story

This is the project where the *safety story* matters as much as the code. Your README should make it impossible to miscategorize this as anything but a controlled simulator. Suggested outline:

```markdown
# AES-256 Ransomware Behavior Simulator (ISC353 P4)

## Team
Abdelrahman Elshabrawi · Mohyaldeen Osman

## Safety statement
- Targets only `./sandbox/test_files/` — verified by `TARGET_DIR` constant
- No network code, no persistence, no registry/cron modification, no self-spread
- Fully reversible: `decrypt_files()` restores originals byte-for-byte
- Runs only inside an isolated VM with no host network; instructor pre-approval on file
- Code reviewed by instructor before first run (M1 evidence)

## What this simulator does
Encrypts files in the sandbox with AES-256-GCM, logs behavioral fingerprints
(SHA-256, original/encrypted entropy, encryption duration) to `behavior_log.jsonl`,
and supports clean decryption.

## How to run
1. `pip install -r requirements.txt`
2. `python ransomware_pro.py` and choose `E` or `D`
3. Inspect `sandbox/behavior_log.jsonl` to see telemetry

## Behavioral signals (feeds M3 YARA detection)
- Entropy delta: encrypted ~7.99 vs original ~4.5 (text) signals encryption activity
- Per-file duration: ~ms range — clusters of fast encryptions = ransomware-like burst
- File rename: original removed, `.locked` appears — atomic rename signature
```

### Suggestion 4 — Add `requirements.txt` and `.gitignore`

```
# requirements.txt
cryptography>=42
```

```
# .gitignore
__pycache__/
*.pyc
.venv/
.env
sandbox/key.bin       # don't ever commit the AES key
sandbox/test_files/*.locked   # don't commit encrypted artifacts; log is enough
!sandbox/test_files/.gitkeep
```

The `.gitignore` exclusion of `sandbox/key.bin` is genuinely important — a committed AES key would be a real finding even on a simulator.

### Suggestion 5 — A small sanity-check addition

Right now `encrypt_files()` will silently re-encrypt files that don't end in `.locked`, but won't refuse to run if `TARGET_DIR` is missing or contains zero files. A 3-line safety check at the top of `encrypt_files()` would tighten the safety story:

```python
def encrypt_files():
    if not os.path.isdir(TARGET_DIR):
        print(f"[!] Refusing to run — sandbox dir {TARGET_DIR} does not exist."); return
    if any(p.startswith("/Users") or p.startswith("/home") for p in [os.path.abspath(TARGET_DIR)]):
        print("[!] Refusing to run — TARGET_DIR resolves outside the sandbox."); return
    aesgcm = AESGCM(get_key())
    # ... rest of your loop
```

Belt-and-suspenders, but the kind of defensive programming I love seeing in safety-critical exercises.

---

## Priority list — what to address first

In this order, starting today:

1. **Re-upload the complete `ransomware_pro.py`** from your local copy (5 minutes, biggest single mark recovery — Technical Correctness moves from 5 to ~20+ if the file actually runs).
2. **Add the `sandbox/test_files/` directory with 2-3 sample files**, run encrypt + decrypt once, and commit `sandbox/behavior_log.jsonl` as evidence.
3. **Add `README.md` with the safety statement** (Suggestion 3 — the *story* matters as much as the code on this project).
4. **Add `requirements.txt` and `.gitignore`** (Suggestion 4 — 5 minutes, real Code Quality marks; the `.gitignore` of `key.bin` is non-negotiable).
5. **Make sure your PDF report and demo video are uploaded to Moodle by 11:59 PM tonight** — those rows account for 55/100 and are currently sitting at 0 in this pregrade only because they're not on GitHub.
6. **Get one real commit in from Abdelrahman's account** before Tuesday's official grading (or document the split clearly in the PDF appendix).

---

## Closing note

Mohyaldeen and Abdelrahman — please don't read the `7/100` as a final judgment. The repo state is brutal at the moment because of the truncated upload, but the *design* visible in the fragment is one of the more careful pieces of work I've seen in this cohort. AES-GCM, fresh nonces, behavioral fingerprinting via entropy delta — these are the right ideas, and you reached for them on your own.

The path back is short: re-upload the complete file, add a sandbox folder with sample data, write a one-page README that makes the safety story explicit. That's a 90-minute task that recovers the bulk of the repo-side rubric, and the 55 marks tied to the PDF + video are entirely yours on Tuesday.

You've got the hard part done (designing the simulator correctly). Let's get it across the line.

— Dr. Shaikhah
