"""
Simple test script to verify the bank statement analyzer functionality.
"""

import os
import json
import sys

def test_demo():
    """Test the demo version of the app."""
    print("Running demo test...")
    
    # Run demo
    os.system("python demo.py > /dev/null 2>&1")
    
    # Check if output folder was created
    if not os.path.exists("extracted_rent_payments"):
        print("❌ FAILED: Output folder not created")
        return False
    
    # Check if summary file exists
    summary_file = "extracted_rent_payments/rent_payments_summary.json"
    if not os.path.exists(summary_file):
        print("❌ FAILED: Summary file not created")
        return False
    
    # Check if summary has valid JSON
    try:
        with open(summary_file, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("❌ FAILED: Summary is not a list")
                return False
            if len(data) == 0:
                print("❌ FAILED: No payments found")
                return False
            
            # Check first payment has required fields
            first_payment = data[0]
            required_fields = ['date', 'amount', 'payee', 'description']
            for field in required_fields:
                if field not in first_payment:
                    print(f"❌ FAILED: Missing field '{field}' in payment")
                    return False
            
            print(f"✅ PASSED: Found {len(data)} rent payment(s)")
            print(f"   Sample payment: {first_payment['date']} - {first_payment['amount']}")
            return True
            
    except json.JSONDecodeError:
        print("❌ FAILED: Invalid JSON in summary file")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_sample_statement():
    """Test that sample statement file exists and is readable."""
    print("\nTesting sample statement file...")
    
    if not os.path.exists("sample_statement.txt"):
        print("❌ FAILED: sample_statement.txt not found")
        return False
    
    try:
        with open("sample_statement.txt", 'r') as f:
            content = f.read()
            if len(content) == 0:
                print("❌ FAILED: sample_statement.txt is empty")
                return False
            
            # Check for rent-related keywords
            keywords = ['rent', 'landlord', 'housing', 'lease']
            found_keywords = [kw for kw in keywords if kw.lower() in content.lower()]
            
            if not found_keywords:
                print("❌ WARNING: No rent keywords found in sample statement")
                return False
            
            print(f"✅ PASSED: Sample statement is valid")
            print(f"   Found keywords: {', '.join(found_keywords)}")
            return True
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def cleanup():
    """Clean up test artifacts."""
    print("\nCleaning up test files...")
    if os.path.exists("extracted_rent_payments"):
        import shutil
        shutil.rmtree("extracted_rent_payments")
        print("✅ Cleaned up output folder")


def main():
    """Run all tests."""
    print("="*60)
    print("Bank Statement Analyzer - Test Suite")
    print("="*60)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    tests_passed = 0
    tests_total = 2
    
    # Run tests
    if test_sample_statement():
        tests_passed += 1
    
    if test_demo():
        tests_passed += 1
    
    # Cleanup
    cleanup()
    
    # Summary
    print("\n" + "="*60)
    print(f"Test Results: {tests_passed}/{tests_total} passed")
    print("="*60)
    
    if tests_passed == tests_total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
