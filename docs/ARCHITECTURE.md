# Identity Disc Vault — Architecture & Design Specification

> Developer secret injector and cloud bootstrap CLI enforcing zero-trust hardware key and Passkey signature verification.

---

## 1. Problem Statement & System Motivation

Developer machines and CI runners frequently store sensitive credentials (API tokens, database credentials, AWS secrets) in plaintext on disk (`.env`, `~/.aws/credentials`).

### 1.1 The Operational Gap
* **Infostealers and Supply Chain Vulnerabilities**: A compromised development tool or malicious build dependency can inspect the local filesystem and exfiltrate static credentials in milliseconds.
* **Absence of User Presence Verification**: Once credentials exist in plaintext or unlocked storage, any rogue background process can impersonate the developer without requiring physical presence or biometric approval.
* **Persistent Credential Sprawl**: Secrets remain on disk indefinitely long after active sessions expire, multiplying exposure vectors over time.

---

## 2. The Solution: Identity Disc Vault Architecture

Identity Disc Vault (`idvault`) enforces zero-trust process execution by marrying physical presence verification with memory-only ephemeral secret injection.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   IDENTITY DISC VAULT INJECTION FLOW                   │
└────────────────────────────────────────────────────────────────────────┘

              Developer / Script / CI Execution
                             │
                             ▼
            ┌───────────────────────────────────┐
            │  idvault exec -- <target command> │
            └─────────────────┬─────────────────┘
                              │
                              ▼
            ┌───────────────────────────────────┐
            │ Hardware Key / Passkey Challenge  │
            │ (Touch ID / YubiKey / WebAuthn)   │
            └─────────────────┬─────────────────┘
                              │ Physical Presence Verified
                              ▼
            ┌───────────────────────────────────┐
            │ In-Memory Envelope Decryption     │
            │ (AES-256-GCM / ChaCha20-Poly1305) │
            │ • RAM locked with `mlock`         │
            └─────────────────┬─────────────────┘
                              │
                              ▼
            ┌───────────────────────────────────┐
            │ Spawn Target Subprocess           │
            │ • Injected into child env / pipe  │
            │ • ZERO DISK WRITE                 │
            │ • Memory auto-zeroized upon exit  │
            └───────────────────────────────────┘
```

### 2.1 Core Architectural Subsystems

1. **Hardware & Biometric Attestation Gate**:
   * Supports FIDO2 / CTAP2 hardware security keys (e.g. YubiKey) requiring physical touch confirmation.
   * Full Passkey / platform authenticator support: Apple Touch ID via Secure Enclave, Windows Hello, and Linux TPM2/FIDO devices.
   * Hardware key is optional: developers can authenticate with local platform Passkeys.
2. **Ephemeral Memory-Only Injection Engine**:
   * Decrypted secrets never touch disk, swap space, or persistent storage.
   * Decrypted memory segments are protected using `mlock` / `VirtualLock` to prevent OS paging to disk.
   * Child processes receive secrets through direct memory environment blocks or anonymous file descriptors (`/dev/fd/X`).
   * Buffers are immediately cleared using constant-time zeroization primitives (`zeroize`) upon command completion.
3. **Cloud Federation Bootstrap**:
   * Exchanging verified hardware-backed authentication tokens for short-lived cloud credentials (AWS STS AssumeRoleWithWebIdentity, GCP Workload Identity).
   * Eliminates the need to maintain static cloud access keys.

---

## 3. Security & Operational Targets

* **Workstation Disk Exposure**: `0 bytes` (Zero plaintext on-disk footprint)
* **Execution Gating**: Physical presence / Biometric passkey required per policy window
* **Memory Protection**: Protected via OS `mlock` and deterministic `zeroize`
* **Injection Overhead**: `< 12 ms` latency addition to target process invocation
