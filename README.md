# Assignment: Manual Bitcoin Key Derivation

## 🎯 Objective

Implement a program that derives a **WIF Private Key** and **P2PKH Bitcoin Address** from raw entropy (a hexadecimal private key). This assignment tests your understanding of:
- Elliptic Curve Cryptography (secp256k1)
- Cryptographic hashing (SHA-256, RIPEMD-160)
- Base58Check encoding
- Bitcoin key standards

---

## 📋 Problem Statement

**Input**: A 64-character hexadecimal string (256-bit private key) provided via **standard input (stdin)**.

**Output**: Three lines printed to **standard output (stdout)**:
```
Compressed PubKey: <33-byte compressed public key in hex>
WIF: <Wallet Import Format Private Key>
Address: <P2PKH Bitcoin Address>
```

### Example

**Input (via stdin)**:
```
0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D
```

**Output (via stdout)**:
```
Compressed PubKey: 02A1B2C3D4E5F6...  (33 bytes as 66 hex chars)
WIF: KwdMAjGmerYveJ...        (Base58Check encoded)
Address: 1LoVGDgRs9hTfT...    (Base58Check encoded)
```

---

## � Security Notice

This assignment uses a **secure testing system** that prevents cheating:

- ✅ **No visible answers**: Test cases use randomly generated private keys  
- ✅ **Server-side validation**: Expected outputs computed during testing, not stored
- ✅ **Anti-cheating**: Students cannot predict or hardcode results
- ✅ **Authentic learning**: Forces implementation of actual cryptographic algorithms
- ✅ **Local testing available**: Students can test implementations privately before submission

Students must implement the complete Bitcoin key derivation process to pass tests.

---

## �🚀 How to Submit

### Step 1: Choose ONE Language

Pick **one** language from the following options:
- Python
- JavaScript (Node.js)
- Go
- Rust
- C++

⚠️ **Important**: You must submit in **only one language**. If you submit multiple solutions, the auto-grader will fail.

### Step 2: Choose Your Language & Implement

Each `solution/` folder contains a ready-to-use template. Pick ONE language and implement the TODO functions:

| Language   | Location & Setup |
|------------|------------------|
| **Python** | `solution/python/main.py`<br>`pip install -r solution/python/requirements.txt` |
| **JavaScript** | `solution/javascript/main.js`<br>`cd solution/javascript && npm install` |
| **Go** | `solution/go/main.go`<br>`cd solution/go && go mod tidy` |
| **Rust** | `solution/rust/main.rs`<br>`cd solution/rust && cargo build` |
| **C++** | `solution/cpp/main.cpp`<br>`g++ -std=c++17 -lssl -lcrypto -lsecp256k1` |

**⚠️ Important**: Remove other language folders before submitting to avoid the "multiple language" error.

### Step 3: Implement the TODOs

Each template has 3 main functions to implement:
- `generate_compressed_pubkey()` - ECDSA secp256k1 + compression
- `generate_wif()` - Wallet Import Format with checksum  
- `generate_address()` - P2PKH address with Base58Check

### Step 4: Test & Submit

```bash
# Test locally (see LOCAL_TESTING.md for detailed guide)
python3 secure_test_runner.py

# OR specify language explicitly (keeps all templates)
LANGUAGE=python python3 secure_test_runner.py

# Clean up (optional - remove unused language folders for final submission)
rm -rf solution/javascript solution/go solution/rust solution/cpp  # if using Python

# Submit
git add solution/
git commit -m "Implement Bitcoin key derivation in Python"
git push origin main
```

The auto-grader will run automatically via GitHub Actions. Check the **Actions** tab to see your results.

---

## 🧪 Testing Locally

You can test your solution locally before pushing:

```bash
python3 test_runner.py
```

The test runner will:
1. Detect which language you used
2. Compile your code (if needed)
3. Run all test cases from `tests.json`
4. Show which tests passed/failed

---

## � Library Restrictions

**⚠️ IMPORTANT**: To ensure you understand Bitcoin cryptography from first principles, you **MUST NOT** use high-level wallet libraries that abstract away the mathematical details.

### ❌ Banned Libraries (Will Cause Submission Failure)

These libraries do too much "magic" and hide the cryptographic steps you need to implement:

#### 🐍 **Python**
- ❌ `bip-utils` - Full BIP39/BIP32/BIP44 implementation
- ❌ `bit` / `bit-wallet` - High-level wallet wrapper
- ❌ `bitcoin` / `pybitcointools` - Complete Bitcoin toolkit
- ❌ `bitcoinlib` - Full wallet management suite
- ❌ `mnemonic` - Use `hashlib` PBKDF2 instead

#### 🟨 **JavaScript/TypeScript**
- ❌ `bitcoinjs-lib` - Standard library (too high-level)
- ❌ `bitcore-lib` - Full node implementation
- ❌ `bip32` / `bip39` - Abstract derivation logic
- ❌ `ethers.js` / `web3.js` - Contain HD wallet functions

#### 🦀 **Rust**
- ❌ `bdk` - Bitcoin Dev Kit (builds whole wallet)
- ❌ `bitcoin` - Main crate with `Address` types
- ❌ `btcaddr` - Specialized address crate

#### 🐹 **Go**
- ❌ `btcsuite/btcwallet` - Full wallet implementation
- ❌ `btcsuite/btcutil` - High-level address functions
- ❌ `tyler-smith/go-bip39` - Automatic seed generation

#### ⚡ **C++**
- ❌ `libbitcoin` - Complete toolkit
- ❌ `libbitcoin-client` / `libbitcoin-wallet`

### ✅ Allowed Libraries (Cryptographic Primitives)

You **MAY** use these low-level libraries that provide cryptographic building blocks:

| Language | **Elliptic Curves** | **Hashing** | **Base58 Encoding** |
|----------|-------------------|-------------|-------------------|
| **Python** | `ecdsa`, `coincurve` | `hashlib` (built-in) | `base58` |
| **JavaScript** | `tiny-secp256k1`, `elliptic` | `crypto` (built-in) | `bs58` |
| **Rust** | `secp256k1`, `k256` | `sha2`, `ripemd`, `hmac` | `bs58` |
| **Go** | `secp256k1/v4` | `crypto/sha256`, `ripemd160` | `base58` (encoding only) |
| **C++** | `libsecp256k1` | `openssl/sha.h`, `openssl/ripemd.h` | Simple copy-paste function |

### 🚨 Automatic Detection

Our test runner **automatically scans** your code for banned imports:

```
🚫 BANNED LIBRARIES DETECTED!
❌ Your solution uses PROHIBITED high-level Bitcoin libraries.

   Line 3: import bitcoin
   ↳ Contains banned library: bitcoin

📚 You must implement Bitcoin address generation manually!
```

**If banned libraries are detected, your submission will be automatically rejected.**

---

## �📚 Implementation Guide

### Required Steps

Your program must perform these cryptographic operations:

#### 1. **Parse the Private Key**
Convert the hexadecimal string to bytes (32 bytes).

#### 2. **Generate Compressed Public Key**
- Use ECDSA on the secp256k1 curve
- Point multiply: `P = k * G` (where G is the generator point)
- Compress the public key:
  - If y-coordinate is even: prefix `0x02`
  - If y-coordinate is odd: prefix `0x03`
- Result: 33 bytes

#### 3. **Generate WIF (Wallet Import Format)**
```
1. Start with version byte: 0x80 (mainnet)
2. Append private key (32 bytes)
3. Append compression flag: 0x01
4. Compute checksum: SHA256(SHA256(version + key + flag))[:4]
5. Concatenate: version + key + flag + checksum
6. Encode with Base58
```

#### 4. **Generate P2PKH Address**
```
1. Compute SHA256 of compressed public key
2. Compute RIPEMD160 of the SHA256 hash (Hash160)
3. Prepend version byte: 0x00 (mainnet P2PKH)
4. Compute checksum: SHA256(SHA256(version + hash160))[:4]
5. Concatenate: version + hash160 + checksum
6. Encode with Base58
```

### Recommended Libraries

**⚠️ Constraint**: You must implement the **full derivation** manually. Do not use high-level wallet libraries like `bitcoinlib`, `bip32`, or `hdkey`.

**Allowed libraries**:
- **Elliptic Curve**: `ecdsa`, `secp256k1`, `elliptic`, `k256`, `secp256k1-crate`
- **Hashing**: `hashlib`, `crypto`, `sha2`, `ripemd`, `openssl`
- **Base58**: `base58`, `bs58`, `base58check`

---

## 🐛 Common Pitfalls

1. **Wrong byte order**: Bitcoin uses big-endian encoding for keys.
2. **Missing compression flag**: WIF for compressed keys needs `0x01` suffix.
3. **Incorrect checksum**: Must use double SHA-256 (SHA256 twice).
4. **Wrong prefix bytes**:
   - WIF mainnet: `0x80`
   - P2PKH mainnet: `0x00`
5. **Reading input incorrectly**: Use `stdin`, not command-line arguments.
6. **Output format**: Must match exactly:
   ```
   Compressed PubKey: <compressed_public_key_hex>
   WIF: <wif>
   Address: <address>
   ```

---

## 📖 Resources

- [Bitcoin Addresses - Technical Background](https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses)
- [Wallet Import Format](https://en.bitcoin.it/wiki/Wallet_import_format)
- [secp256k1 Curve Parameters](https://en.bitcoin.it/wiki/Secp256k1)
- [Base58Check encoding](https://en.bitcoin.it/wiki/Base58Check_encoding)

---

## ❓ FAQ

**Q: Can I use multiple files?**
A: Yes, but your main entry point must be named `main.py`, `main.js`, etc.

**Q: Can I use external dependencies?**
A: Yes, but add them to `requirements.txt` (Python) or `package.json` (JavaScript).

**Q: What if my tests fail?**
A: Check the GitHub Actions logs for detailed error messages. Compare your output with expected output.

**Q: Can I test with custom inputs?**
A: Yes! Run your program manually:
```bash
echo "YOUR_HEX_KEY" | python3 solution/python/main.py
```

---

## 📊 Grading

Your submission is graded automatically:
- ✅ **3/3 tests pass** = Full marks
- ⚠️ **2/3 tests pass** = Partial credit
- ❌ **0-1 tests pass** = Needs revision

Good luck! 🚀
