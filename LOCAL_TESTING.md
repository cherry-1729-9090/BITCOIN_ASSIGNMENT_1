# Local Testing Guide for Students

## 🧪 How to Test Your Implementation Locally

### Prerequisites
Before testing, ensure you have the required dependencies:

**For Python**: 
```bash
pip install ecdsa base58
```

**For JavaScript**:
```bash
cd solution/javascript
npm install
```

**For Go**:
```bash
cd solution/go
go mod tidy
```

**For Rust**:
```bash
cd solution/rust
cargo build
```

**For C++**:
```bash
# Ubuntu/Debian
sudo apt-get install libssl-dev libsecp256k1-dev

# macOS
brew install openssl libsecp256k1
```

### Step 1: Choose Your Testing Method

**Option A: Quick Test Script (Easiest)**
```bash
# Auto-detect your implementation
./test.sh

# Or specify language explicitly  
./test.sh python
./test.sh javascript
./test.sh go
./test.sh rust
./test.sh cpp
```

**Option B: Smart Detection**
The test runner automatically detects which language you've implemented:
```bash
python3 secure_test_runner.py
```

**Option C: Explicit Language Selection**
Specify which language to test (keeps all templates):
```bash
LANGUAGE=python python3 secure_test_runner.py
LANGUAGE=javascript python3 secure_test_runner.py
LANGUAGE=go python3 secure_test_runner.py
LANGUAGE=rust python3 secure_test_runner.py
LANGUAGE=cpp python3 secure_test_runner.py
```

**Option D: Remove Other Languages (Traditional)**
Keep only ONE language folder in `solution/`:
```bash
# Example: If using Python, remove other languages
rm -rf solution/javascript solution/go solution/rust solution/cpp
python3 secure_test_runner.py
```

### What You'll See

#### ✅ **Successful Test Run**
```
🎓 Secure Bitcoin Key Derivation Test Runner
============================================
✓ Detected language: PYTHON
✓ Solution file: solution/python/main.py
🔒 SECURE TEST MODE - Answers Hidden From Students
============================================================

🧪 Test 1: Running with private key 911FEE4E7D508AE3...
✅ All outputs correct!

🧪 Test 2: Running with private key 645A4E1D632A720D...
✅ All outputs correct!

🧪 Test 3: Running with private key 911E567FDD78E2FB...
✅ All outputs correct!

📊 RESULTS: 3/3 tests passed
🎉 Congratulations! Your implementation is correct.
```

#### ❌ **Templates Not Implemented**
```
❌ No implemented solutions found!

💡 All detected files appear to be unmodified templates:
  - python: solution/python/main.py
  - javascript: solution/javascript/main.js
  - go: solution/go/main.go

📝 Please implement the TODO functions in your chosen language.
   Or set LANGUAGE environment variable: LANGUAGE=python python3 secure_test_runner.py
```

#### ❌ **Multiple Implementations**
```
❌ Multiple implemented solutions detected!

⚠️  You have implementations in:
  - python: solution/python/main.py
  - go: solution/go/main.go

📋 Options:
   1. Keep only ONE implementation and remove others
   2. Use LANGUAGE environment variable:
      LANGUAGE=python python3 secure_test_runner.py
      LANGUAGE=go python3 secure_test_runner.py
```

#### ❌ **Failed Test Run**
```
🔒 SECURE TEST MODE - Answers Hidden From Students
============================================================

🧪 Test 1: Running with private key 911FEE4E7D508AE3...
❌ Incorrect cryptographic outputs
  - Compressed public key incorrect
  - WIF private key incorrect
  - Bitcoin address incorrect

📊 RESULTS: 0/3 tests passed
🔧 Please fix your cryptographic implementation.

💡 HINTS:
- Double-check secp256k1 public key generation
- Verify WIF includes compression flag (0x01)
- Ensure proper Hash160 for address generation
- Validate Base58Check encoding with correct checksums
```

#### 🚫 **Banned Library Detection**
```
BANNED LIBRARY DETECTED: 'import bitcoin' in solution/python/main.py

You are using prohibited libraries!
```

### Key Features of Local Testing

1. **🔒 Secure**: You cannot see the expected outputs - just pass/fail feedback
2. **🎲 Random**: Each test run uses different private keys
3. **🚫 Anti-cheat**: Cannot hardcode answers since they change every time
4. **⚡ Fast**: Get immediate feedback on your implementation
5. **📝 Detailed**: Clear error messages guide you toward fixes

### Testing Workflow

1. **Implement** functions in your chosen language
2. **Test locally** with `python3 secure_test_runner.py`
3. **Debug** using the hint messages
4. **Iterate** until all tests pass
5. **Commit and push** to trigger GitHub Actions

### Common Issues

- **Format errors**: Make sure output matches exact format requirements
- **Import errors**: Install required dependencies
- **Compilation errors**: Fix syntax issues before testing
- **Timeout errors**: Optimize your implementation if tests take too long

### Why Local Testing is Important

- ✅ **Immediate feedback** - No waiting for GitHub Actions
- ✅ **Unlimited attempts** - Test as many times as needed  
- ✅ **Privacy** - Test your incomplete code without public failures
- ✅ **Learning aid** - Understand what's wrong with hint messages
- ✅ **Efficiency** - Fix issues before final submission

Remember: The local tests use the same secure system as GitHub Actions, so passing locally means your implementation is correct!