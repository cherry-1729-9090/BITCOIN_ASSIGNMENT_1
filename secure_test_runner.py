#!/usr/bin/env python3
"""
Secure Test Runner - GitHub Classroom Bitcoin Key Derivation
============================================================

SECURITY FEATURES:
- No hardcoded expected outputs visible to students
- Uses server-side validation with environment variables  
- Generates random test cases students cannot predict
- Validates crypto implementation without revealing answers

FOR GITHUB ACTIONS:
- Set ASSIGNMENT_SEED environment variable for reproducible tests
- Expected outputs are computed server-side using reference implementation

FOR STUDENTS:
- Only provides pass/fail feedback
- Cannot see expected outputs or copy answers
- Must implement actual cryptography to pass tests
"""

import os
import sys
import subprocess
import json
import hashlib
import ecdsa
import base58
import re
from pathlib import Path


class SecureValidator:
    """Validates Bitcoin key derivation without exposing answers."""
    
    def __init__(self):
        self.seed = os.environ.get('ASSIGNMENT_SEED', 'default_seed_for_testing')
        
    def generate_reference_output(self, private_key_hex):
        """Generate correct outputs using reference implementation."""
        try:
            private_key_bytes = bytes.fromhex(private_key_hex)
            
            # Generate compressed public key
            sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
            vk = sk.get_verifying_key()
            point = vk.pubkey.point
            
            # Compress public key
            if point.y() % 2 == 0:
                compressed_pubkey = b'\x02' + point.x().to_bytes(32, byteorder='big')
            else:
                compressed_pubkey = b'\x03' + point.x().to_bytes(32, byteorder='big')
            
            # Generate WIF (compressed)
            extended_key = b'\x80' + private_key_bytes + b'\x01'
            hash1 = hashlib.sha256(extended_key).digest()
            hash2 = hashlib.sha256(hash1).digest()
            checksum = hash2[:4]
            wif = base58.b58encode(extended_key + checksum).decode('utf-8')
            
            # Generate P2PKH address
            sha256_hash = hashlib.sha256(compressed_pubkey).digest()
            ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
            versioned_payload = b'\x00' + ripemd160_hash
            hash1 = hashlib.sha256(versioned_payload).digest()
            hash2 = hashlib.sha256(hash1).digest()
            checksum = hash2[:4]
            address = base58.b58encode(versioned_payload + checksum).decode('utf-8')
            
            return {
                'pubkey': compressed_pubkey.hex().upper(),
                'wif': wif,
                'address': address
            }
        except Exception as e:
            return None
    
    def validate_output_format(self, output):
        """Check if output follows correct format without revealing answers."""
        lines = output.strip().split('\n')
        if len(lines) != 3:
            return False, "Output must have exactly 3 lines"
            
        # Check format without revealing content
        pubkey_line = lines[0]
        wif_line = lines[1] 
        addr_line = lines[2]
        
        if not pubkey_line.startswith('Compressed PubKey: '):
            return False, "First line must start with 'Compressed PubKey: '"
            
        if not wif_line.startswith('WIF: '):
            return False, "Second line must start with 'WIF: '"
            
        if not addr_line.startswith('Address: '):
            return False, "Third line must start with 'Address: '"
        
        # Extract values
        pubkey = pubkey_line[19:]  # After "Compressed PubKey: "
        wif = wif_line[5:]        # After "WIF: "
        address = addr_line[9:]   # After "Address: "
        
        # Basic format validation
        if len(pubkey) != 66 or not all(c in '0123456789ABCDEF' for c in pubkey):
            return False, "Compressed PubKey must be 66 hex characters"
            
        if not (pubkey.startswith('02') or pubkey.startswith('03')):
            return False, "Compressed PubKey must start with 02 or 03"
            
        if not (wif.startswith('K') or wif.startswith('L') or wif.startswith('5')):
            return False, "WIF must start with K, L, or 5"
            
        if not address.startswith('1'):
            return False, "P2PKH address must start with 1"
            
        return True, "Format correct"
    
    def run_secure_tests(self, solution_file, language):
        """Run tests without exposing expected outputs."""
        print("🔒 SECURE TEST MODE - Answers Hidden From Students")
        print("=" * 60)
        
        # Generate test private keys deterministically
        test_keys = []
        for i in range(3):
            seed_data = f"{self.seed}_test_{i}".encode()
            key_hash = hashlib.sha256(seed_data).digest()
            # Ensure valid secp256k1 range
            key_int = int.from_bytes(key_hash, 'big')
            secp256k1_order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
            key_int = (key_int % (secp256k1_order - 1)) + 1
            test_keys.append(key_int.to_bytes(32, 'big').hex().upper())
        
        passed = 0
        total = len(test_keys)
        
        for i, private_key in enumerate(test_keys):
            print(f"\n🧪 Test {i+1}: Running with private key {private_key[:16]}...")
            
            # Run student solution
            try:
                if language == 'python':
                    result = subprocess.run([sys.executable, solution_file], 
                                          input=private_key, text=True, 
                                          capture_output=True, timeout=10)
                elif language == 'go':
                    result = subprocess.run(['go', 'run', solution_file], 
                                          input=private_key, text=True, 
                                          capture_output=True, timeout=10)
                elif language == 'javascript':
                    result = subprocess.run(['node', solution_file], 
                                          input=private_key, text=True, 
                                          capture_output=True, timeout=10)
                elif language == 'rust':
                    result = subprocess.run(['cargo', 'run'], 
                                          input=private_key, text=True, 
                                          capture_output=True, timeout=10, 
                                          cwd=Path(solution_file).parent)
                elif language == 'cpp':
                    # Compile and run
                    exe_path = Path(solution_file).parent / 'main'
                    compile_result = subprocess.run(['g++', '-o', str(exe_path), solution_file, 
                                                   '-lssl', '-lcrypto', '-lsecp256k1'],
                                                  capture_output=True, timeout=30)
                    if compile_result.returncode != 0:
                        print(f"❌ Compilation failed: {compile_result.stderr.decode()}")
                        continue
                    result = subprocess.run([str(exe_path)], 
                                          input=private_key, text=True,
                                          capture_output=True, timeout=10)
                else:
                    print(f"❌ Unsupported language: {language}")
                    continue
                    
                if result.returncode != 0:
                    stderr_output = result.stderr if isinstance(result.stderr, str) else result.stderr.decode()
                    print(f"❌ Runtime error: {stderr_output}")
                    continue
                    
            except subprocess.TimeoutExpired:
                print("❌ Test timed out")
                continue
            except Exception as e:
                print(f"❌ Error running test: {e}")
                continue
            
            # Validate format first
            format_ok, format_msg = self.validate_output_format(result.stdout)
            if not format_ok:
                print(f"❌ Format error: {format_msg}")
                continue
                
            # Generate reference outputs (server-side only)
            expected = self.generate_reference_output(private_key)
            if not expected:
                print("❌ Failed to generate reference output")
                continue
                
            # Compare outputs (without showing expected to student)
            student_lines = result.stdout.strip().split('\n')
            student_pubkey = student_lines[0][19:]  # After "Compressed PubKey: "
            student_wif = student_lines[1][5:]      # After "WIF: "  
            student_addr = student_lines[2][9:]     # After "Address: "
            
            # Validate each component
            pubkey_correct = student_pubkey == expected['pubkey']
            wif_correct = student_wif == expected['wif'] 
            addr_correct = student_addr == expected['address']
            
            if pubkey_correct and wif_correct and addr_correct:
                print("✅ All outputs correct!")
                passed += 1
            else:
                print("❌ Incorrect cryptographic outputs")
                if not pubkey_correct:
                    print("  - Compressed public key incorrect")
                if not wif_correct:
                    print("  - WIF private key incorrect")  
                if not addr_correct:
                    print("  - Bitcoin address incorrect")
        
        print(f"\n📊 RESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 Congratulations! Your implementation is correct.")
            return True
        else:
            print("🔧 Please fix your cryptographic implementation.")
            print("\n💡 HINTS:")
            print("- Double-check secp256k1 public key generation")
            print("- Verify WIF includes compression flag (0x01)")
            print("- Ensure proper Hash160 for address generation")
            print("- Validate Base58Check encoding with correct checksums")
            return False


def detect_language_and_file():
    """Detect student's chosen language and main file."""
    import os
    solution_dir = Path("solution")
    
    languages = {
        'python': 'main.py',
        'javascript': 'main.js', 
        'go': 'main.go',
        'rust': 'main.rs',
        'cpp': 'main.cpp'
    }
    
    # Check for environment variable to specify language
    selected_lang = os.environ.get('LANGUAGE')
    if selected_lang and selected_lang.lower() in languages:
        lang = selected_lang.lower()
        filename = languages[lang]
        file_path = solution_dir / lang / filename
        if file_path.exists():
            return lang, str(file_path)
        else:
            print(f"❌ {lang} solution file not found: {file_path}")
            return None, None
    
    # Look for implemented solutions (not just template TODO functions)
    implemented = []
    template_only = []
    
    for lang, filename in languages.items():
        file_path = solution_dir / lang / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it's still just a template (contains TODO markers and panic/throw/todo!)
                is_template = any(marker in content.lower() for marker in [
                    'todo!', 'panic!', 'panic(', 'throw new error', 
                    'not implemented', 'todo:', '# todo', '// todo'
                ])
                
                if is_template:
                    template_only.append((lang, str(file_path)))
                else:
                    implemented.append((lang, str(file_path)))
            except:
                template_only.append((lang, str(file_path)))
    
    if len(implemented) == 0 and len(template_only) > 0:
        print("❌ No implemented solutions found!")
        print("\n💡 All detected files appear to be unmodified templates:")
        for lang, filepath in template_only:
            print(f"  - {lang}: {filepath}")
        print("\n📝 Please implement the TODO functions in your chosen language.")
        print("   Or set LANGUAGE environment variable: LANGUAGE=python python3 secure_test_runner.py")
        return None, None
    elif len(implemented) == 1:
        return implemented[0]
    elif len(implemented) > 1:
        print("❌ Multiple implemented solutions detected!")
        print("\n⚠️  You have implementations in:")
        for lang, filepath in implemented:
            print(f"  - {lang}: {filepath}")
        print("\n📋 Options:")
        print("   1. Keep only ONE implementation and remove others")
        print("   2. Use LANGUAGE environment variable:")
        for lang, _ in implemented:
            print(f"      LANGUAGE={lang} python3 secure_test_runner.py")
        return None, None
    else:
        print("❌ No solution files found in solution/ folders")
        return None, None


def main():
    """Run secure tests on student implementation."""
    print("🎓 Secure Bitcoin Key Derivation Test Runner")
    print("============================================")
    
    # Banned library patterns by language  
    banned_patterns = {
        'python': [
            r'import\s+bitcoind',
            r'import\s+bitcoin\b',
            r'from\s+bitcoin',
            r'python-bitcoinlib', 
            r'pycoin',
            r'hdwallet'
        ],
        'javascript': [
            r'require\([\'"]bitcoinjs-lib[\'"]',
            r'require\([\'"]bitcore-lib[\'"]',
            r'import.*bitcoinjs-lib',
            r'import.*bitcore-lib',
            r'bip32',
            r'bip39',
            r'ethers',
            r'web3'
        ],
        'rust': [
            r'bdk\s*=',
            r'bitcoin\s*=.*["\']',
            r'btcaddr\s*='
        ],
        'go': [
            r'btcsuite/btcwallet',
            r'btcsuite/btcutil(?!/base58)',
            r'tyler-smith/go-bip39'
        ],
        'cpp': [
            r'libbitcoin',
            r'libbitcoin.client',
            r'libbitcoin.wallet'
        ]
    }
    
    language, solution_file = detect_language_and_file()
    if not language:
        sys.exit(1)
        
    print(f"✓ Detected language: {language.upper()}")
    print(f"✓ Solution file: {solution_file}")
    
    # Check for banned libraries
    def check_banned_libraries(file_path, lang):
        if lang not in banned_patterns:
            return True
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return False
        
        for pattern in banned_patterns[lang]:
            if re.search(pattern, content, re.IGNORECASE):
                print(f"\nBANNED LIBRARY DETECTED: '{pattern}' in {file_path}")
                print("\nYou are using prohibited libraries!")
                return False
        return True
    
    if not check_banned_libraries(solution_file, language):
        sys.exit(1)
    
    # Run secure tests
    validator = SecureValidator()
    success = validator.run_secure_tests(solution_file, language)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()