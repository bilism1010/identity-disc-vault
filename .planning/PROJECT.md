# Identity Disc Vault - Project Blueprint

## 1. Vision & Core Value Proposition
**Identity Disc Vault (`idvault`)** is an ephemeral developer secret injector and cloud bootstrap CLI enforcing zero-trust hardware key (FIDO2 / U2F / YubiKey) and Passkey (WebAuthn / Apple Secure Enclave / Windows Hello) verification.
Inspired by the TRON identity disc, an entity's identity, permissions, and cryptographic capabilities are inextricably tied to hardware-backed attestation and user presence (touch / biometric), eliminating plaintext secrets from workstation disks, shell histories, and dotfiles.

## 2. Core Functional Requirements
1. **Multi-Modal Authenticator Support**:
   - Hardware security keys via FIDO2/CTAP2 over USB HID.
   - Native platform Passkeys via Apple Secure Enclave / Touch ID (macOS Keychain / CryptoKit), Windows Hello, or Linux secret-service/TPM2.
   - Optional passkey-only or hardware-key-only operation modes.
2. **Envelope Cryptography & Key Management**:
   - Zero-knowledge local vault format (`.idvault/`).
   - Root Data Encryption Key (DEK) wrapped by Key Encryption Keys (KEK) derived from enrolled authenticators.
   - Multi-device recovery and secondary key enrollment (e.g., primary YubiKey + backup Passkey).
3. **In-Memory Subprocess Injection (`idvault exec`)**:
   - Secrets decrypted only after active User Presence (UP) / User Verification (UV) attestation.
   - Transient in-memory injection into target child processes (environment variables or anonymous pipes `/dev/fd/X`) without touching storage.
   - Guaranteed zeroization (`zeroize`) and strict protection against memory dumps/swap.
4. **Cloud Bootstrapping & Dynamic Ephemeral Credentials**:
   - Hardware-attested assertion exchanged for short-lived cloud sessions (AWS STS AssumeRole with Web Identity / OIDC, GCP Workload Identity Federation, HashiCorp Vault).

## 3. High-Level Architecture & Modules
- `idvault-core`: Cryptographic primitives, envelope encryption, memory protection (`mlock`, `zeroize`), serialization.
- `idvault-auth`: Authenticator abstraction trait (`AuthenticatorBackend`) with implementations for CTAP2/FIDO2 HID and OS Passkeys / Secure Enclave.
- `idvault-store`: Local vault layout, multi-profile schema, ACL policies, profile inheritance.
- `idvault-injector`: Process spawning, IPC pipes, environment sanitization, parent/child safety.
- `idvault-cloud`: Ephemeral credential brokers (AWS STS, GCP WIF, Vault).
- `idvault-cli`: Clap-based CLI binary (`idvault`).
