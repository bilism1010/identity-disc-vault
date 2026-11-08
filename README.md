# Identity Disc Vault

> Zero-trust developer secret injector and cloud bootstrap CLI enforcing hardware key (FIDO2/U2F / YubiKey) and Passkey (WebAuthn/Secure Enclave) signature verification.

Inspired by the TRON identity disc — an immutable representation of an entity's identity, permissions, and cryptographic capabilities.

---

## 1. Goal

Eliminate long-lived plain-text secrets (API keys, cloud tokens, database credentials, SSH certificates) from developer local workstations and CI environments. Provide an ephemeral, hardware-backed environment injection engine where secrets are cryptographically tied to user presence (Touch ID / FIDO2 YubiKey / WebAuthn Passkeys) and injected directly into target processes in-memory without touching disk.

---

## 2. Specification

### 2.1 Core Capabilities
- **Hardware / Passkey Attestation**:
  - Support FIDO2 / CTAP2 hardware tokens (YubiKey, SoloKey, Nitrokey) with User Verification (PIN / biometric) and User Presence (touch).
  - Native Passkey / Secure Enclave integration (Apple Touch ID via keychain/CryptoKit, Windows Hello, Linux TPM2/FIDO).
- **Ephemeral Process Injection**:
  - Subprocess execution wrapper (`idvault exec -- <cmd>`) injecting decrypted secrets straight into child environment variables or named in-memory pipes (`/dev/fd/X` or platform equivalent) without persistent disk writes.
  - Zeroization of all secret buffers upon process fork/exec.
- **Envelope Encryption**:
  - Vault files encrypted using AES-256-GCM / ChaCha20-Poly1305 with data encryption keys (DEK) wrapped by hardware/passkey-backed public keys (secp256r1 / ed25519).
- **Cloud Bootstrap & Dynamic Lease**:
  - Integrations with cloud IAM (AWS STS AssumeRole with Web Identity, GCP Workload Identity, HashiCorp Vault) triggered via short-lived attested hardware assertions.

### 2.2 CLI Architecture & Commands
- `idvault init`: Initialize vault root and enroll authenticators (Passkey / FIDO2).
- `idvault auth enroll`: Register primary and fallback hardware keys or passkeys.
- `idvault secret set <KEY> <VALUE>`: Encrypt and store key-value pair under policy.
- `idvault exec [--profile <p>] -- <command>`: Prompt hardware touch, decrypt, and launch child process with transient secrets.
- `idvault cloud assume <target-role>`: Mint ephemeral cloud credential session based on hardware signature.

---

## 3. Recommended Prompt for Next Refinement Phase

```text
Act as a Principal Security and Systems Engineer. We are designing 'Identity Disc Vault', a Rust-based zero-trust CLI for ephemeral secret injection and cloud bootstrapping authenticated via FIDO2 and Passkeys.
Please produce:
1. Detailed threat model (memory dumps, ptrace injection, authenticator clone resistance, compromised parent shell).
2. Cross-platform authenticator abstraction layer design (ctap-hid-fido2 vs Apple Secure Enclave / WebAuthn passkey).
3. Memory safety & zeroization strategy (e.g., zeroize, mlock/VirtualLock, seccomp/pledge).
4. CLI UX specification and reference mock implementation of `idvault exec`.
```

---

## 4. Scaffolding & Getting Started

```bash
# Verify Rust toolchain
cargo check

# Run tests
cargo test

# Build debug binary
cargo run -- --help
```
