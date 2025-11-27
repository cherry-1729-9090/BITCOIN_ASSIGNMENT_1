//! Bitcoin Key Derivation - Rust Template
//! ========================================
//! 
//! TODO: Implement Bitcoin address generation from raw private key
//! 
//! Your program should:
//! 1. Read a hexadecimal private key from stdin
//! 2. Generate a compressed public key using secp256k1
//! 3. Generate a WIF (Wallet Import Format) private key
//! 4. Generate a P2PKH Bitcoin address
//! 5. Output both WIF and address to stdout
//! 
//! ALLOWED libraries (add to Cargo.toml):
//! - secp256k1 or k256: For secp256k1 elliptic curve operations
//! - sha2, ripemd: For SHA-256 and RIPEMD-160 hashing
//! - bs58: For Base58Check encoding
//! 
//! FORBIDDEN libraries (will cause automatic failure):
//! - bdk, bitcoin, btcaddr
//! 
//! Expected output format:
//! Compressed PubKey: <compressed_public_key_hex>
//! WIF: <wallet_import_format>
//! Address: <p2pkh_address>

use std::io::{self, Read};
// TODO: Import allowed libraries (secp256k1, sha2, ripemd, bs58)

/// Generate compressed public key from private key.
/// 
/// Steps:
/// 1. Use secp256k1 curve to get public key point (x, y)
/// 2. Compress: 0x02 + x if y is even, 0x03 + x if y is odd
/// 
/// # Arguments
/// * `private_key_bytes` - 32-byte private key
/// 
/// # Returns  
/// * 33-byte compressed public key
fn generate_compressed_pubkey(private_key_bytes: &[u8; 32]) -> [u8; 33] {
    // TODO: Implement secp256k1 point multiplication
    // TODO: Implement public key compression
    todo!("Implement compressed public key generation")
}

/// Generate Wallet Import Format from private key.
/// 
/// Steps:
/// 1. Add version byte 0x80 (mainnet)
/// 2. Add private key (32 bytes)
/// 3. Add compression flag 0x01
/// 4. Calculate checksum: first 4 bytes of SHA256(SHA256(data))
/// 5. Base58 encode the result
/// 
/// # Arguments
/// * `private_key_bytes` - 32-byte private key
/// 
/// # Returns
/// * Base58-encoded WIF string
fn generate_wif(private_key_bytes: &[u8; 32]) -> String {
    // TODO: Implement WIF generation
    // TODO: Use double SHA-256 for checksum
    // TODO: Use Base58 encoding
    todo!("Implement WIF generation")
}

/// Generate P2PKH address from compressed public key.
/// 
/// Steps:
/// 1. SHA-256 hash of public key
/// 2. RIPEMD-160 hash of SHA-256 result (Hash160)
/// 3. Add version byte 0x00 (P2PKH mainnet)
/// 4. Calculate checksum: first 4 bytes of SHA256(SHA256(data))
/// 5. Base58 encode the result
/// 
/// # Arguments
/// * `compressed_pubkey` - 33-byte compressed public key
/// 
/// # Returns
/// * Base58-encoded P2PKH address
fn generate_address(compressed_pubkey: &[u8; 33]) -> String {
    // TODO: Implement Hash160 (SHA256 + RIPEMD160)
    // TODO: Add version byte and checksum
    // TODO: Use Base58 encoding
    todo!("Implement P2PKH address generation")
}

fn main() -> io::Result<()> {
    // Read private key from stdin
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    
    let private_key_hex = input.trim();
    
    // Parse hex string to bytes
    let private_key_bytes = match hex::decode(private_key_hex) {
        Ok(bytes) if bytes.len() == 32 => {
            let mut array = [0u8; 32];
            array.copy_from_slice(&bytes);
            array
        }
        _ => {
            eprintln!("Error: Private key must be 32 bytes (64 hex chars)");
            std::process::exit(1);
        }
    };
    
    // TODO: Generate compressed public key
    let compressed_pubkey = generate_compressed_pubkey(&private_key_bytes);
    
    // TODO: Generate WIF
    let wif = generate_wif(&private_key_bytes);
    
    // TODO: Generate address
    let address = generate_address(&compressed_pubkey);
    
    // Output in required format
    println!("Compressed PubKey: {}", hex::encode(&compressed_pubkey).to_uppercase());
    println!("WIF: {}", wif);
    println!("Address: {}", address);
    
    Ok(())
}