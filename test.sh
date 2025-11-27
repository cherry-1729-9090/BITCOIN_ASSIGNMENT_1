#!/bin/bash
# Quick test script for students - no need to delete language folders!

echo "🎓 Bitcoin Key Derivation - Quick Test"
echo "======================================"

# Check if a specific language was requested
if [ "$1" != "" ]; then
    echo "Testing $1 implementation..."
    LANGUAGE=$1 python3 secure_test_runner.py
    exit $?
fi

# Auto-detect implemented solution
echo "Auto-detecting your implementation..."
python3 secure_test_runner.py
result=$?

if [ $result -ne 0 ]; then
    echo ""
    echo "💡 TIP: If you have multiple implementations, specify which to test:"
    echo "   ./test.sh python"
    echo "   ./test.sh javascript" 
    echo "   ./test.sh go"
    echo "   ./test.sh rust"
    echo "   ./test.sh cpp"
fi

exit $result