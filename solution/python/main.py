#!/usr/bin/env python3
"""
Bitcoin Key Derivation - Python Template
=========================================

TODO: Implement Bitcoin address generation from raw private key

Your program should:
1. Read a hexadecimal private key from stdin
2. Generate a compressed public key using secp256k1
3. Generate a WIF (Wallet Import Format) private key  
4. Generate a P2PKH Bitcoin address
5. Output both WIF and address to stdout

ALLOWED libraries (install via: pip install -r requirements.txt):
- ecdsa: For secp256k1 elliptic curve operations
- base58: For Base58Check encoding
- hashlib: For SHA-256 and RIPEMD-160 hashing (built-in)

FORBIDDEN libraries (will cause automatic failure):
- bitcoin, bitcoinlib, bit, bip-utils, mnemonic

Expected output format:
Compressed PubKey: <compressed_public_key_hex>
WIF: <wallet_import_format>
Address: <p2pkh_address>
"""

import sys
import hashlib
# TODO: Import allowed libraries (ecdsa, base58)


def generate_compressed_pubkey(private_key_bytes):
    """
    Generate compressed public key from private key.
    
    Steps:
    1. Use ECDSA secp256k1 to get public key point (x, y)
    2. Compress: 0x02 + x if y is even, 0x03 + x if y is odd
    
    Args:
        private_key_bytes: 32-byte private key
    
    Returns:
        33-byte compressed public key
    """
    # TODO: Implement secp256k1 point multiplication
    # TODO: Implement public key compression
    pass


def generate_wif(private_key_bytes):
    """
    Generate Wallet Import Format from private key.
    
    Steps:
    1. Add version byte 0x80 (mainnet)
    2. Add private key (32 bytes)  
    3. Add compression flag 0x01
    4. Calculate checksum: first 4 bytes of SHA256(SHA256(data))
    5. Base58 encode the result
    
    Args:
        private_key_bytes: 32-byte private key
        
    Returns:
        Base58-encoded WIF string
    """
    # TODO: Implement WIF generation
    # TODO: Use double SHA-256 for checksum
    # TODO: Use Base58 encoding
    pass


def generate_address(compressed_pubkey):
    """
    Generate P2PKH address from compressed public key.
    
    Steps:
    1. SHA-256 hash of public key
    2. RIPEMD-160 hash of SHA-256 result (Hash160)
    3. Add version byte 0x00 (P2PKH mainnet)
    4. Calculate checksum: first 4 bytes of SHA256(SHA256(data))
    5. Base58 encode the result
    
    Args:
        compressed_pubkey: 33-byte compressed public key
        
    Returns:
        Base58-encoded P2PKH address
    """
    # TODO: Implement Hash160 (SHA256 + RIPEMD160)
    # TODO: Add version byte and checksum
    # TODO: Use Base58 encoding
    pass


def main():
    """
    Main function: Read from stdin, generate WIF and address, print to stdout.
    """
    # Read private key from stdin
    try:
        private_key_hex = sys.stdin.read().strip()
        private_key_bytes = bytes.fromhex(private_key_hex)
        
        if len(private_key_bytes) != 32:
            print("Error: Private key must be 32 bytes (64 hex chars)", file=sys.stderr)
            sys.exit(1)
            
    except ValueError:
        print("Error: Invalid hexadecimal input", file=sys.stderr)
        sys.exit(1)
    
    # TODO: Generate compressed public key
    compressed_pubkey = generate_compressed_pubkey(private_key_bytes)
    
    # TODO: Generate WIF
    wif = generate_wif(private_key_bytes)
    
    # TODO: Generate address
    address = generate_address(compressed_pubkey)
    
    # Output in required format
    print(f"Compressed PubKey: {compressed_pubkey.hex().upper()}")
    print(f"WIF: {wif}")
    print(f"Address: {address}")


if __name__ == '__main__':
    main()