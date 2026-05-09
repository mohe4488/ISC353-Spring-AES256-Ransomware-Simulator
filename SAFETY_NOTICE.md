⚠️ SAFETY NOTICE — PLEASE READ BEFORE CLONING

# WARNING: RANSOMWARE SIMULATOR CODE

This repository contains an **AES-256 ransomware behavior simulator** designed for **educational purposes only** as part of coursework at Kuwait University (ISC 353 — Information Security).

---

## ⚠️ CRITICAL WARNINGS

### 1. **DO NOT CLONE TO YOUR HOST MACHINE**
- **ONLY** run this code inside an **isolated, air-gapped virtual machine** (VM).
- This simulator encrypts files using real AES-256-GCM cryptography.
- Even though it is hardcoded to target only `./sandbox/test_files/`, unforeseen circumstances could cause data loss.
- If you are unsure how to set up a secure VM environment, **DO NOT USE THIS CODE**.

### 2. **Potential for Data Loss**
- This code implements **real file encryption** with AES-256-GCM.
- While decryption functionality is provided, mistakes in deployment or modifications to the code could result in **permanent data loss**.
- The developers assume **no responsibility** for data loss caused by misuse or improper execution.

### 3. **Educational Use Only**
- This simulator is part of an academic cybersecurity course and is submitted as coursework.
- Any use outside of controlled educational or authorized security research environments is **prohibited**.
- Unauthorized use for malicious purposes is illegal and unethical.

### 4. **Not a Standalone Product**
- This is a research/educational tool, not production software.
- The code has **not undergone security audits** for deployment outside isolated VMs.
- No guarantees of stability, compatibility, or safety in production environments.

---

## 📋 What This Simulator Does

This code **simulates** the behavior of ransomware in a **controlled sandbox** to:
1. Generate cryptographic behavior telemetry for malware analysis
2. Create ground-truth data for YARA detection rule development
3. Educate students on how ransomware encryption/decryption mechanics work

**It is NOT:**
- A malware distribution tool
- A tool for encrypting real data outside controlled environments
- Licensed for commercial use
- Intended for use on production systems

---

## ✅ Safety Guarantees (As Designed)

The simulator includes hardcoded protections:

| Safety Control | Implementation |
|---|---|
| **Scope-Limited** | Only targets `./sandbox/test_files/` directory |
| **No Network Activity** | Zero socket/network calls in codebase |
| **No Persistence** | No registry, cron, or startup modifications |
| **No Self-Propagation** | Cannot spread beyond target directory |
| **Fully Reversible** | Complete decryption with SHA-256 verification |
| **Isolated Execution** | Must run in isolated VM with no host network access |
| **Instructor Reviewed** | Code pre-approved by ISC 353 course instructor |

---

## 🚫 RISKS & DISCLAIMERS

### Risks of Cloning This Repository:

1. **Accidental Execution**: If run outside a VM or with modified paths, this could encrypt important files.
2. **Code Modifications**: Any modifications to the hardcoded safety constraints could disable protections.
3. **Zero-Day Vulnerabilities**: While no known vulnerabilities exist, cryptographic code may have unforeseen issues.
4. **Dependency Vulnerabilities**: The `cryptography` library and Python environment could have security issues.
5. **Improper Environment Setup**: Inadequate VM isolation could allow the simulator to impact host systems.

### Who Should NOT Clone This Repository:

- ❌ Users without VM virtualization experience
- ❌ Users on production systems or systems with valuable data
- ❌ Users without isolated, air-gapped network environments
- ❌ Users intending to use this for any non-educational purpose
- ❌ Users who cannot review and understand the Python code before execution
- ❌ Users in jurisdictions where cryptographic tools are restricted

---

## ✅ Prerequisites & Safe Usage

If you choose to proceed, ensure you have:

- ✅ **Isolated VM Setup**: VirtualBox, VMware, or similar with no shared folders/network access to host
- ✅ **Linux Distribution**: Kali Linux, Ubuntu, or similar (recommended: fresh installation)
- ✅ **Python 3.8+**: Installed in the VM
- ✅ **No Valuable Data**: Sandbox directories contain **only test files** you can afford to lose
- ✅ **Code Review**: You have reviewed `ransomware_pro.py` line-by-line and understand what it does
- ✅ **Backup Plan**: You can restore the VM from a snapshot if needed
- ✅ **Air-Gapped Network**: The VM is **not connected** to any network or shared drives

### Step-by-Step Safe Deployment:

1. **Create a New VM** with dedicated storage (no host access)
2. **Take a Snapshot** before cloning this repo
3. **Clone the Repository** only inside the VM:
   ```bash
   git clone https://github.com/mohe4488/ISC353-Spring-AES256-Ransomware-Simulator.git
   ```
4. **Review the Code** (especially ransomware_pro.py)
5. **Prepare Test Data**: Place only test/dummy files in sandbox/test_files/
6. **Run the Simulator**: Follow instructions in README.md
7. **Restore from Snapshot** if anything goes wrong
## 📖 Terms of Use & Legal
This project is:

✅ Licensed under MIT License for academic use only
✅ Submitted as official coursework at Kuwait University (ISC 353)
✅ Available for educational review and non-malicious security research
Users agree to:

1. Use only in isolated, controlled environments
2. Not redistribute without proper attribution
3. Not use for any malicious, illegal, or unauthorized purpose
4. Assume full responsibility for their own use and any consequences
Developers disclaim:

1. Liability for data loss or system damage
2. Responsibility for misuse or unauthorized deployment
3. Obligation to provide support or updates
## 📞 Questions or Concerns?
If you have safety concerns or questions before cloning:

Review the complete README.md for technical details
Contact the course instructor (ISC 353 at Kuwait University)
Do not attempt to run this code if you have any doubts about your environment
## 🎓 Educational Context
This simulator was developed as part of ISC 353: Information Security at Kuwait University, specifically for:

Team: Abdelrahman Elshabrawi, Mohyaldeen Osman

Phase: Milestone 2 — Core Build (Milestone 3 will develop YARA detection rules)

Instructor: Pre-approved for controlled academic use only


---

By cloning this repository, you acknowledge that:


✅ You understand the risks

✅ You are running this in an isolated VM environment

✅ You have read and understood all warnings

✅ You assume full responsibility for any consequences

✅ You will not use this code for malicious purposes

If you do not agree to these terms, please DO NOT CLONE THIS REPOSITORY.


---

**Last Updated:** 2026-05-09  
**Repository:** [mohe4488/ISC353-Spring-AES256-Ransomware-Simulator](https://github.com/mohe4488/ISC353-Spring-AES256-Ransomware-Simulator)
