#!/bin/bash
# 
# Simple Banned Library Checker for CI/CD Pipeline
# =================================================
# This script provides basic enforcement of banned libraries.
# 
# Usage: ./check_banned_simple.sh
# Exit code: 0 (clean) or 1 (banned libraries found)

echo "🔍 Scanning for banned Bitcoin libraries..."

BANNED_FOUND=0

# Check Python files
echo "🐍 Checking Python files..."
if find solution/python -name "*.py" -exec grep -l -E "(import|from).*(bip.?utils?|bit[^a-z]|bitcoin[^j]|bitcoinlib|mnemonic)" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo "    ❌ BANNED Python libraries detected!"
    find solution/python -name "*.py" -exec grep -H -E "(import|from).*(bip.?utils?|bit[^a-z]|bitcoin[^j]|bitcoinlib|mnemonic)" {} \; 2>/dev/null | head -5
    BANNED_FOUND=1
else
    echo "    ✅ Python files clean"
fi

# Check JavaScript files  
echo "🟨 Checking JavaScript files..."
if find solution/javascript -name "*.js" -exec grep -l -E "(require|import).*(bitcoinjs-lib|bitcore-lib|bip32|bip39|ethers|web3)" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo "    ❌ BANNED JavaScript libraries detected!"
    find solution/javascript -name "*.js" -exec grep -H -E "(require|import).*(bitcoinjs-lib|bitcore-lib|bip32|bip39|ethers|web3)" {} \; 2>/dev/null | head -5
    BANNED_FOUND=1
else
    echo "    ✅ JavaScript files clean"
fi

# Check Rust files
echo "🦀 Checking Rust files..."
if find solution/rust -name "*.rs" -exec grep -l -E "(use|extern crate).*(bdk|bitcoin[^a-z]|btcaddr)" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo "    ❌ BANNED Rust libraries detected!"
    find solution/rust -name "*.rs" -exec grep -H -E "(use|extern crate).*(bdk|bitcoin[^a-z]|btcaddr)" {} \; 2>/dev/null | head -5
    BANNED_FOUND=1
else
    echo "    ✅ Rust files clean"
fi

# Check Go files
echo "🐹 Checking Go files..."
if find solution/go -name "*.go" -exec grep -l -E "import.*\".*btc.*\"" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo "    ❌ BANNED Go libraries detected!"
    find solution/go -name "*.go" -exec grep -H -E "import.*\".*btc.*\"" {} \; 2>/dev/null | head -5
    BANNED_FOUND=1
else
    echo "    ✅ Go files clean"
fi

# Check C++ files
echo "⚡ Checking C++ files..."
if find solution/cpp -name "*.cpp" -o -name "*.hpp" -o -name "*.h" | xargs grep -l "#include.*libbitcoin" 2>/dev/null | head -1 | grep -q .; then
    echo "    ❌ BANNED C++ libraries detected!"
    find solution/cpp -name "*.cpp" -o -name "*.hpp" -o -name "*.h" | xargs grep -H "#include.*libbitcoin" 2>/dev/null | head -5
    BANNED_FOUND=1
else
    echo "    ✅ C++ files clean"
fi

echo ""
if [[ $BANNED_FOUND -eq 1 ]]; then
    echo "🚫 BANNED LIBRARIES DETECTED!"
    echo "   Your submission uses prohibited high-level Bitcoin libraries."
    echo "   Please use only the allowed cryptographic primitives."
    echo "   See README.md for the complete list of allowed libraries."
    exit 1
else
    echo "✅ No banned libraries detected. Good job!"
    exit 0
fi