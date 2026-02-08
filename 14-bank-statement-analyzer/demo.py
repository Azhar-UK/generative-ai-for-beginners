"""
Test/Demo version of the bank statement analyzer.
This version simulates AI responses for demonstration without requiring an API key.
"""

import json
import os
from datetime import datetime


def mock_extract_rent_payments(statement_text):
    """
    Mock version that simulates AI extraction for demonstration.
    In a real scenario, this would use the OpenAI API.
    """
    
    # Simple keyword-based extraction for demonstration
    rent_payments = []
    
    lines = statement_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        # Look for rent-related keywords
        if any(keyword in line_lower for keyword in ['rent', 'landlord', 'housing', 'lease']):
            # Try to extract basic information
            parts = line.split()
            
            # Look for date pattern
            date = None
            amount = None
            description = line.strip()
            
            for part in parts:
                # Look for date (simple MM/DD/YY pattern)
                if '/' in part and len(part.split('/')) == 3:
                    date_parts = part.split('/')
                    try:
                        month, day, year = date_parts
                        if len(year) == 2:
                            year = '20' + year
                        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    except (ValueError, IndexError):
                        pass
                
                # Look for amount (contains $ or decimal)
                if '$' in part or (part.replace(',', '').replace('.', '').replace('-', '').isdigit() and '.' in part):
                    amount = part.replace('$', '').strip()
            
            if date:  # Only add if we found a date
                payment = {
                    "date": date,
                    "amount": amount or "N/A",
                    "payee": "Extracted from statement",
                    "description": description,
                    "reference": "Auto-detected rent payment"
                }
                rent_payments.append(payment)
    
    return rent_payments


def save_rent_payments(rent_payments, output_folder="extracted_rent_payments"):
    """
    Save extracted rent payments to individual files in a folder.
    """
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Save summary file
    summary_file = os.path.join(output_folder, "rent_payments_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(rent_payments, f, indent=2)
    
    print(f"\n✅ Summary saved to: {summary_file}")
    
    # Save individual payment files
    for i, payment in enumerate(rent_payments, 1):
        date_str = payment.get('date', 'unknown').replace('-', '')
        filename = f"rent_payment_{date_str}_{i}.json"
        filepath = os.path.join(output_folder, filename)
        
        with open(filepath, 'w') as f:
            json.dump(payment, f, indent=2)
        
        print(f"   - {filename}")
    
    print(f"\n📁 Total {len(rent_payments)} rent payment(s) extracted to '{output_folder}' folder")


def read_statement_file(filepath):
    """
    Read bank statement from a file.
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def main():
    """
    Main function to run the bank statement analyzer demo.
    """
    print("=== Bank Statement Rent Payment Extractor (DEMO MODE) ===")
    print("This demo uses keyword matching instead of AI for demonstration.\n")
    
    # Check for sample statement file
    sample_file = "sample_statement.txt"
    
    if os.path.exists(sample_file):
        print(f"📄 Using statement file: {sample_file}\n")
        statement_text = read_statement_file(sample_file)
    else:
        print("📄 Using example bank statement\n")
        statement_text = """
        Bank Statement - January 2024
        
        Date       Description                          Amount    Balance
        ----------------------------------------------------------------
        01/05/24   RENT PAYMENT - ABC PROPERTIES       -1,500.00  8,500.00
        01/08/24   GROCERY STORE                         -85.50  8,414.50
        01/10/24   SALARY DEPOSIT                     +3,500.00 11,914.50
        01/15/24   UTILITIES - ELECTRIC                 -120.00 11,794.50
        01/20/24   LANDLORD - MONTHLY RENT             -1,500.00 10,294.50
        01/25/24   RESTAURANT                            -45.00 10,249.50
        01/28/24   GAS STATION                           -60.00 10,189.50
        """
    
    if statement_text:
        print("🔍 Analyzing statement for rent payments...\n")
        
        # Extract rent payments using mock function
        rent_payments = mock_extract_rent_payments(statement_text)
        
        if rent_payments:
            print(f"Found {len(rent_payments)} rent payment(s):\n")
            for i, payment in enumerate(rent_payments, 1):
                print(f"{i}. Date: {payment.get('date', 'N/A')}")
                print(f"   Amount: {payment.get('amount', 'N/A')}")
                print(f"   Payee: {payment.get('payee', 'N/A')}")
                print(f"   Description: {payment.get('description', 'N/A')}\n")
            
            # Save to files
            save_rent_payments(rent_payments)
            
            print("\n" + "="*60)
            print("Demo completed successfully!")
            print("="*60)
            print("\nTo use the full AI-powered version:")
            print("1. Set up your OpenAI API key in a .env file")
            print("2. Run 'python app.py' instead")
            print("\nSee README.md for detailed instructions.")
        else:
            print("No rent payments found in the statement.")
    else:
        print("Unable to process bank statement.")


if __name__ == "__main__":
    main()
