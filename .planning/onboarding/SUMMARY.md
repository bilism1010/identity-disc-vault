# OpenGSD Onboarding Summary: Identity Disc Vault

## Summary
- **Repository**: `identity-disc-vault`
- **Focus**: Developer secret injector and cloud bootstrap CLI enforcing zero-trust hardware key signature verification (FIDO2) and native Passkeys (Touch ID / Secure Enclave).
- **Toolchain**: Rust (2021 edition), `clap`, `zeroize`, `serde`.
- **Planning Files Created**:
  - `.planning/PROJECT.md`
  - `.planning/REQUIREMENTS.md`
  - `.planning/ROADMAP.md`
  - `.planning/STATE.md`

## Next Actions
1. Deep-dive technical questions to resolve core architecture decisions.
2. Threat modeling and cryptography envelope specification.
3. Authenticator substrate selection for macOS (Secure Enclave / Touch ID) vs Linux/Windows (FIDO2 / TPM).
