# System Requirements: Identity Disc Vault

## Functional Requirements (FR)
- **FR1: Authenticator Enrollment & Attestation**
  - FR1.1: Enroll FIDO2/CTAP2 tokens via USB/NFC with User Presence (UP) check.
  - FR1.2: Enroll OS-native Passkeys (macOS Secure Enclave / Touch ID, Windows Hello) as primary or secondary authenticators.
  - FR1.3: Support multiple enrolled authenticators per vault with threshold or M-of-N/1-of-N unlock capabilities.
- **FR2: Secret Storage & Cryptographic Envelope**
  - FR2.1: Encrypt secrets using standard authenticated encryption (AES-256-GCM or ChaCha20-Poly1305).
  - FR2.2: Decrypt DEK only upon valid hardware attestation / WebAuthn assertion signature.
  - FR2.3: Support structured namespaces, environment profiles (e.g., `prod`, `staging`), and tags.
- **FR3: Ephemeral Process Execution (`exec`)**
  - FR3.1: Launch arbitrary commands with injected environment variables without writing secrets to `.env` or disk.
  - FR3.2: Support file descriptor injection (`/dev/fd/N` or named in-memory pipes) for tools that reject env vars.
  - FR3.3: Ensure zeroization of decrypted secret buffers on process exit or termination.
- **FR4: Cloud Attestation & Bootstrap**
  - FR4.1: Mint signed assertion tokens to exchange with cloud STS providers (AWS STS, GCP STS) for temporary credentials.

## Non-Functional Requirements (NFR)
- **NFR1: Security & Anti-Leakage**: Secure memory regions against swap paging (`mlock`), zero memory on drop (`zeroize`), restrict ptrace / debugger attachment where feasible.
- **NFR2: Performance**: Sub-second unlock overhead beyond physical hardware touch latency (<50ms processing).
- **NFR3: Portability**: Tier-1 support for macOS (Apple Silicon & Intel) and Linux (x86_64, aarch64); Tier-2 Windows.
- **NFR4: Usability & Ergonomics**: Clear CLI prompts for physical touch / biometric verification; seamless drop-in for commands like `idvault exec -- terraform apply`.
