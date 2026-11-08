# Roadmap: Identity Disc Vault

## Phase Overview

- [ ] **Phase 1: Security Architecture, Threat Model & Cryptographic Spec**
  - Deep threat modeling (memory dumps, ptrace injection, authenticator clone resistance, compromised parent shell).
  - Define vault envelope file format, key derivation, and multi-key recovery structure.
  - Rust memory isolation, zeroization, and OS security boundaries (`mlock`, `MADV_DONTDUMP`).

- [ ] **Phase 2: Hardware & Passkey Abstraction Layer**
  - Authenticator abstraction trait (`AuthenticatorBackend`).
  - Native macOS Secure Enclave / Touch ID / LocalAuthentication integration.
  - Cross-platform FIDO2 / CTAP2 HID implementation (`ctap-hid-fido2` or `authenticator-rs`).
  - Interactive enrollment and attestation verification workflows.

- [ ] **Phase 3: Vault Core Storage & Secret Management**
  - Local vault initialization (`idvault init`) and storage engine.
  - Profile-based secret CRUD (`idvault secret set/get/list/delete`).
  - Multi-authenticator key wrapping (envelope encryption).

- [ ] **Phase 4: Ephemeral Process Injector (`idvault exec`)**
  - In-memory environment variable injection for child processes.
  - Process spawning, signal handling, and execution isolation.
  - Optional file descriptor / in-memory pipe redirection (`/dev/fd/X`).
  - Strict buffer zeroization upon process launch and cleanup.

- [ ] **Phase 5: Cloud Identity & Bootstrap Integration**
  - Attested session token generation.
  - AWS STS AssumeRoleWithWebIdentity / dynamic credentials provider.
  - GCP Workload Identity Federation / HashiCorp Vault connectors.

- [ ] **Phase 6: Developer Ergonomics, Auditing & CLI Polish**
  - Shell completions, TUI touch status indicators.
  - Audit logging of access events (without leaking secret values).
  - End-to-end integration test harness with mock authenticators.
