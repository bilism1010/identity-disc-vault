use clap::{Parser, Subcommand};

#[derive(Parser, Debug)]
#[command(name = "idvault", author, version, about = "Identity Disc Vault - Zero-trust hardware-backed secret injector")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand, Debug)]
pub enum Commands {
    /// Initialize a new Identity Disc vault
    Init {
        #[arg(short, long, default_value = ".idvault")]
        vault_path: String,
    },
    /// Enroll an authenticator (Passkey / FIDO2 hardware key)
    Enroll {
        #[arg(short, long)]
        name: String,
        #[arg(long, default_value_t = false)]
        passkey: bool,
    },
    /// Set a secret in the vault
    Set {
        key: String,
        value: Option<String>,
    },
    /// Execute a command with decrypted secrets injected into memory
    Exec {
        #[arg(short, long)]
        profile: Option<String>,
        #[arg(last = true, required = true)]
        command: Vec<String>,
    },
}

fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    let cli = Cli::parse();
    match cli.command {
        Commands::Init { vault_path } => {
            println!("[Identity Disc Vault] Initializing vault directory at {}", vault_path);
        }
        Commands::Enroll { name, passkey } => {
            let auth_type = if passkey { "Passkey / Secure Enclave" } else { "FIDO2 Hardware Key" };
            println!("[Identity Disc Vault] Enrolling authenticator '{}' using {}", name, auth_type);
        }
        Commands::Set { key, .. } => {
            println!("[Identity Disc Vault] Storing encrypted secret for key '{}'", key);
        }
        Commands::Exec { profile, command } => {
            println!(
                "[Identity Disc Vault] Requesting presence check (profile={:?}) to execute: {:?}",
                profile,
                command.join(" ")
            );
        }
    }
    Ok(())
}
