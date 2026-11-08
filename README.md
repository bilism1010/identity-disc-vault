<div align="center">

```text
██╗██████╗     ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗
██║██╔══██╗    ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝
██║██║  ██║    ██║   ██║███████║██║   ██║██║     ██║   
██║██║  ██║    ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   
██║██████╔╝     ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   
╚═╝╚═════╝       ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   
```

### **ZERO-TRUST DEVELOPER SECRET INJECTOR & HARDWARE IDENTITY VAULT**

[![Rust](https://img.shields.io/badge/RUST-1.75%2B-00e5ff?style=for-the-badge&logo=rust&logoColor=white&labelColor=03060f)](https://www.rust-lang.org/)
[![Status](https://img.shields.io/badge/STATUS-ACTIVE%20RESEARCH-18a0ff?style=for-the-badge&labelColor=03060f)](https://github.com/bsommers)
[![Security](https://img.shields.io/badge/AUTHENTICATION-FIDO2%20%7C%20PASSKEY%20%7C%20TPM-00e5ff?style=for-the-badge&labelColor=03060f)](#the-solution)
[![Zero-Trust](https://img.shields.io/badge/SECRETS-ZERO%20ON--DISK%20EXPOSURE-00e5ff?style=for-the-badge&labelColor=03060f)](#performance-targets)

<p align="center">
  <img src="assets/identity-disc.png" alt="Identity Disc Vault Conceptual Visualization" width="480" />
</p>

<p align="center">
  <b>Developer secret injector and cloud bootstrap CLI enforcing zero-trust hardware key (FIDO2/U2F/YubiKey) and Passkey signature verification.</b><br>
  <i>Inspired by the TRON Identity Disc: your cryptographic essence, your immutable signature, and absolute control over every privileged execution.</i>
</p>

---

## 🛠️ Physical Realization & Hardware Architecture

We have engineered a realistic, open-source physical realization of the TRON Identity Disc as a 3D-printable FIDO2/WebAuthn PRF hardware security vault:

<p align="center">
  <img src="assets/technical-cutaway.png" alt="Identity Disc Technical Cutaway Drawing" width="720" />
</p>

- **Interactive 3D Models**: Production-ready [`.STL`](file:///Users/bill/src/research/systems-programming/indentity-disc-vault/hardware/cad/identity_disc_assembly.stl) and [`.OBJ`](file:///Users/bill/src/research/systems-programming/indentity-disc-vault/hardware/cad/identity_disc_assembly.obj) files for base chassis, top lid, and 360° light ring diffuser in [`hardware/cad/`](file:///Users/bill/src/research/systems-programming/indentity-disc-vault/hardware/cad/).
- **Bill of Materials (BoM)**: Complete prototype BOM (~$15.30 total cost) leveraging the ESP32-S3 (Native USB HID + Crypto), ATECC608B Secure Element, and 16x addressable LEDs in [`hardware/bom/BILL_OF_MATERIALS.md`](file:///Users/bill/src/research/systems-programming/indentity-disc-vault/hardware/bom/BILL_OF_MATERIALS.md).
- **Presence Verification**: Integrated capacitive touch electrode for FIDO2 User Presence (UP) checks.

---

</div>

## ⚡ The Problem Statement

Developer workstations and CI/CD runners represent the soft underbelly of modern software supply chains. The current state of secrets management is structurally vulnerable:

```text
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│     Current Developer Reality   │ vs  │    Sophisticated Attack Vector  │
│ (Plaintext .env, Shell Exports) │     │ (Infostealers, CI Compromises)  │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ ❌ Plaintext `.env` / `.aws`    │     │ ❌ Infostealer malware scanning │
│ ❌ Long-lived API tokens on disk│     │ ❌ Unattended shell exfiltration│
│ ❌ Persistent SSH & cloud keys  │     │ ❌ Accidental git commits       │
│ ❌ No presence / touch gating   │     │ ❌ Rogue dependency escalation  │
└─────────────────────────────────┘     └─────────────────────────────────┘
```

1. **Persistent Plaintext Secrets on Disk**: Developers routinely store high-privilege credentials (AWS access keys, production database passwords, Stripe/GitHub tokens) in plaintext dotfiles (`~/.aws/credentials`, `.env`, `.bashrc`). One malicious npm dependency or infostealer malware strain instantly harvests the entire fleet.
2. **Missing Proof-of-Presence Gating**: Once written to disk, credentials can be read repeatedly without any user knowledge or physical authorization. There is no cryptographic verification that the authorized human is actively sitting in front of the console during execution.
3. **Complex Cloud Bootstrapping Friction**: Developers bypass security policies because authenticating to cloud IAM roles (AWS STS, GCP Workload Identity, Vault) requires tedious token dances, encouraging users to fallback to long-lived static API keys.

---

## 💡 The Solution: Identity Disc Vault

**Identity Disc Vault (`idvault`)** eliminates permanent secrets from workstation disks entirely. Secrets are cryptographically bound to hardware security keys (FIDO2/YubiKey) or biometric Passkeys (Apple Touch ID / Windows Hello / TPM2), and injected ephemerally into child processes in-memory.

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      IDENTITY DISC VAULT ARCHITECTURE                  │
 └────────────────────────────────────────────────────────────────────────┘

                 Developer CLI / Script Execution
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  idvault exec [--profile prod] -- ./deploy-service               │
    └───────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  CRYPTOGRAPHIC IDENTITY ATTESTATION (Physical Presence Gate)     │
    │  • FIDO2 / CTAP2 Token (YubiKey Touch)                           │
    │  • Platform Passkey (Apple Touch ID / Secure Enclave / Win Hello)│
    │  • Signature challenge-response verification                     │
    └───────────────────────────┬──────────────────────────────────────┘
                                │ Verified User Presence
                                ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  ENVELOPE DECRYPTION & EPHEMERAL SECRET GENERATION               │
    │  • AES-256-GCM / ChaCha20-Poly1305 envelope decryption           │
    │  • Dynamic cloud token exchange (AWS STS / GCP Workload Identity)│
    │  • Memory lock (`mlock`) against swap & OS core dumping          │
    └───────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │  EPHEMERAL PROCESS INJECTION                                     │
    │  • Subprocess launched with in-memory environment variables      │
    │  • Ephemeral anonymous pipes (`/dev/fd/X`) for file credentials  │
    │  • ZERO DISK WRITE & Automatic Zeroization upon exit             │
    └──────────────────────────────────────────────────────────────────┘
```

### Architectural Pillars

* **Hardware & Passkey-Enforced Presence**:
  * Decryption requires explicit physical touch on a FIDO2 hardware token or biometric verification via platform Passkey (Apple Touch ID / Secure Enclave, Windows Hello).
  * Hardware keys are optional; developers without physical YubiKeys seamlessly authenticate via native Passkeys or TPM2 modules.
* **Ephemeral Zero-Disk Process Injection**:
  * Target commands execute as child processes where secrets are injected straight into process memory structures or transient anonymous file descriptors (`/dev/fd/X`).
  * No secrets ever touch disk or swap space; memory buffers are protected with `mlock` and automatically cleared with `zeroize` on process teardown.
* **Cryptographic Envelope Vault**:
  * Vault payloads are encrypted with AES-256-GCM / ChaCha20-Poly1305 using short-lived Data Encryption Keys (DEK) wrapped by hardware/passkey-backed asymmetric keys.
* **Seamless Cloud Identity Bootstrap**:
  * Dynamic exchange transforms verified local hardware signatures into short-lived cloud credentials (AWS STS AssumeRoleWithWebIdentity, GCP Workload Identity, Vault tokens).

---

## 📊 Security & Performance Profile

| Attribute | Specification | Assurance |
| :--- | :--- | :--- |
| **Disk Footprint of Secrets** | `0 bytes` | Secrets exist strictly in locked RAM for process lifespan |
| **User Presence Assurance** | `Cryptographic (FIDO2 / Passkey)` | Hardware-backed signature required per session/execution |
| **Memory Protection** | `mlock + Zeroize on drop` | Immune to OS paging to disk, swap leaks, or core dumps |
| **Injection Overhead** | `< 12 ms` | Near-zero latency addition to target command invocation |
| **Cloud IAM Federation** | `AWS STS, GCP, Vault` | Ephemeral credential minting replacing static root keys |

---

## 🛠️ Scaffolding & Quickstart

```bash
# 1. Verify Rust toolchain
cargo check

# 2. Run test suite
cargo test

# 3. Initialize vault and enroll primary Passkey / FIDO2 token
cargo run -- init

# 4. Enroll fallback hardware key or platform Passkey
cargo run -- auth enroll

# 5. Store an encrypted credential
cargo run -- secret set AWS_SECRET_ACCESS_KEY "AKIAEXAMPLE1234567"

# 6. Execute command with ephemeral secret injection (prompts for Touch/Passkey)
cargo run -- exec -- env | grep AWS
```

---

## 🔮 Next Refinement Phase Prompt

```text
Act as a Principal Security and Systems Engineer. We are designing 'Identity Disc Vault', a Rust-based zero-trust CLI for ephemeral secret injection and cloud bootstrapping authenticated via FIDO2 and Passkeys.
Please produce:
1. Detailed threat model (memory dumps, ptrace injection, authenticator clone resistance, compromised parent shell).
2. Cross-platform authenticator abstraction layer design (ctap-hid-fido2 vs Apple Secure Enclave / WebAuthn passkey).
3. Memory safety & zeroization strategy (e.g., zeroize, mlock/VirtualLock, seccomp/pledge).
4. CLI UX specification and reference mock implementation of `idvault exec`.
```

---

<div align="center">
<sub>SYSTEM NOTICE: IDENTITY DISC SYNCHRONIZED &bull; ZERO-TRUST PERIMETER SECURED</sub>
</div>
