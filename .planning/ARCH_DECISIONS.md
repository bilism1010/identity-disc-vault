# Architectural Decisions & Technical Foundations: Identity Disc Vault

## 1. Selected Authenticator Strategy
- **Platform-wide WebAuthn / Passkeys**:
  - Leverages OS WebAuthn client APIs (Apple AuthenticationServices on macOS, Windows WebAuthn APIs on Windows, and FIDO2/CTAP2 or secret-service on Linux).
  - Software Passkeys backed by platform biometrics (Touch ID / Windows Hello) alongside physical hardware keys (YubiKeys) behaving as WebAuthn authenticators.

## 2. Key Derivation & Unsealing Protocol
- **WebAuthn PRF (Pseudo-Random Function) Extension**:
  - Uses the W3C WebAuthn PRF extension (`hmac-secret` in CTAP2) to derive an authenticator-specific symmetric Key Encryption Key (KEK).
  - When the developer authenticates with user presence/biometrics, the authenticator outputs a deterministic shared secret from a vault salt.
  - KEK unwraps the Vault Data Encryption Key (DEK).
  - Multi-authenticator enrollments (e.g. secondary passkey) store multiple wrapped copies of the same DEK.

## 3. Subprocess Secret Injection Architecture
- **In-Memory Environment Variables**: Direct inheritance into the spawned child process using `std::process::Command::envs(...)`, zeroing parent copies after exec.
- **Anonymous In-Memory Pipes (`/dev/fd/N`)**: For applications requiring file paths or secrets outside env vars, `idvault` exposes ephemeral read-only file descriptors backed by non-disk pipes.

## 4. Security Enforcements
- Zeroization (`zeroize::Zeroize`, `zeroize::ZeroizeOnDrop`) on all memory buffers containing unsealed DEKs and plaintext secrets.
- `mlock` / `MADV_DONTDUMP` memory isolation to prevent secrets from reaching core dumps or swap files.
