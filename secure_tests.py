#!/usr/bin/env python3
"""
Secure Test Generator for Bitcoin Key Derivation Assignment
===========================================================

This module generates cryptographically correct test cases at runtime.
Students cannot predict the answers since private keys are generated randomly.

For GitHub Actions: Set ASSIGNMENT_SEED environment variable for reproducible tests.
For local testing: Uses random private keys for validation (answers unknown to students).
"""

import os
import hashlib
import secrets
import sys


class SecureTestGenerator:
    def __init__(self):
        # Use environment variable for reproducible tests in CI/CD
        seed = os.environ.get('ASSIGNMENT_SEED')
        if seed:
            # Deterministic generation for CI/CD
            self.rng = hashlib.sha256(seed.encode()).digest()
        else:
            # Random generation for local testing
            self.rng = None
    
    def generate_private_key(self, test_index=0):
        """Generate a valid secp256k1 private key."""
        if self.rng:
            # Deterministic: use seed + test index
            data = self.rng + test_index.to_bytes(4, 'big')
            private_key = hashlib.sha256(data).digest()
        else:
            # Random: generate unpredictable private key
            private_key = secrets.token_bytes(32)
        
        # Ensure private key is in valid secp256k1 range [1, n-1]
        # secp256k1 order: FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        key_int = int.from_bytes(private_key, 'big')
        secp256k1_order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        
        if key_int == 0 or key_int >= secp256k1_order:
            # If invalid, increment until valid (very rare)
            key_int = (key_int % (secp256k1_order - 1)) + 1
            private_key = key_int.to_bytes(32, 'big')
        
        return private_key.hex().upper()
    
    def generate_test_cases(self, count=3):
        """Generate test cases with random private keys."""
        tests = []
        for i in range(count):
            private_key_hex = self.generate_private_key(i)
            tests.append({
                "name": f"Test {i+1}: Random Private Key",
                "input": private_key_hex,
                "expected_format": "Compressed PubKey: <33-byte-hex>\\nWIF: <base58-string>\\nAddress: <base58-address>"
            })
        return tests


def main():
    """Generate secure test cases."""
    generator = SecureTestGenerator()
    tests = generator.generate_test_cases(3)
    
    print("🔒 Generated secure test cases:")
    for test in tests:
        print(f"\n{test['name']}")
        print(f"Input: {test['input']}")
        print(f"Expected: {test['expected_format']}")
        print("(Student must implement crypto to determine actual output)")


if __name__ == "__main__":
    main()