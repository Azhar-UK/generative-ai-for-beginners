# Bank Statement Rent Payment Extractor - Usage Examples

This document provides additional examples and use cases for the bank statement analyzer.

## Example 1: Basic Usage with Demo

```bash
# Run the demo version
python demo.py
```

Expected output:
- Identifies 3 rent payments from the sample statement
- Creates `extracted_rent_payments/` folder
- Saves individual JSON files for each payment
- Creates a summary JSON file

## Example 2: Custom Bank Statement Format

Create a new file `my_statement.txt` with your bank data:

```
Monthly Statement - February 2024
Date        Description                     Amount
02/01/24    Monthly Rent - Main Street     -$2,000.00
02/05/24    Grocery Store                   -$150.00
02/10/24    Apartment Rent Payment         -$2,000.00
```

Then modify the code to use your file:
```python
statement_text = read_statement_file("my_statement.txt")
```

## Example 3: Processing Multiple Statements

Create a simple script to process multiple files:

```python
import os
from app import extract_rent_payments, save_rent_payments, read_statement_file

statement_files = ["jan_statement.txt", "feb_statement.txt", "mar_statement.txt"]

for filename in statement_files:
    if os.path.exists(filename):
        print(f"Processing {filename}...")
        statement_text = read_statement_file(filename)
        rent_payments = extract_rent_payments(statement_text)
        
        # Save with unique folder per month
        month = filename.split('_')[0]
        save_rent_payments(rent_payments, f"rent_{month}")
```

## Example 4: Extracting Different Transaction Types

Modify the prompt to extract utilities instead of rent:

```python
prompt = f"""Analyze the following bank statement and extract all utility-related payments.
Look for keywords like "electric", "gas", "water", "utilities", "sewage", etc.

Bank Statement:
{statement_text}

Return the results as a JSON array...
"""
```

## Example 5: Export to CSV

Add this function to export results to CSV:

```python
import csv

def export_to_csv(rent_payments, filename="rent_payments.csv"):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['date', 'amount', 'payee', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for payment in rent_payments:
            writer.writerow({
                'date': payment.get('date', ''),
                'amount': payment.get('amount', ''),
                'payee': payment.get('payee', ''),
                'description': payment.get('description', '')
            })
    print(f"Exported to {filename}")
```

## Example 6: Filtering by Date Range

Add date range filtering:

```python
from datetime import datetime

def filter_by_date_range(rent_payments, start_date, end_date):
    """
    Filter rent payments by date range.
    
    Args:
        rent_payments: List of payment dictionaries
        start_date: Start date as string "YYYY-MM-DD"
        end_date: End date as string "YYYY-MM-DD"
    
    Returns:
        Filtered list of payments
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    filtered = []
    for payment in rent_payments:
        payment_date = datetime.strptime(payment['date'], "%Y-%m-%d")
        if start <= payment_date <= end:
            filtered.append(payment)
    
    return filtered

# Usage
filtered = filter_by_date_range(rent_payments, "2024-01-01", "2024-01-31")
```

## Example 7: Calculate Total Rent Paid

```python
def calculate_total_rent(rent_payments):
    """Calculate total amount paid in rent."""
    total = 0.0
    for payment in rent_payments:
        amount_str = payment.get('amount', '0')
        # Remove currency symbols and commas
        amount_str = amount_str.replace('$', '').replace(',', '')
        try:
            # Handle negative amounts
            amount = abs(float(amount_str))
            total += amount
        except ValueError:
            print(f"Could not parse amount: {amount_str}")
    
    return total

# Usage
total = calculate_total_rent(rent_payments)
print(f"Total rent paid: ${total:,.2f}")
```

## Tips for Better Results

### 1. Clean Your Bank Statement
- Remove headers/footers that aren't transactions
- Keep consistent date format
- Ensure amounts are clearly formatted

### 2. Improve AI Prompt
- Add specific landlord names if known
- Include apartment number or unit
- Specify typical rent amount range

### 3. Handle Edge Cases
- Multiple rent payments per month (if splitting with roommate)
- Partial rent payments
- Rent credits or refunds

### 4. Privacy Best Practices
- Anonymize names and account numbers
- Don't commit real statements to git
- Clear output folder after use

## Common Issues and Solutions

**Issue**: AI doesn't detect some rent payments
**Solution**: Add more keywords to the prompt or provide examples

**Issue**: False positives (non-rent transactions detected)
**Solution**: Be more specific in the prompt about what constitutes rent

**Issue**: Incorrect date parsing
**Solution**: Standardize date format in your statement before processing

**Issue**: API rate limits
**Solution**: Add delays between API calls when processing multiple files

## Advanced: Batch Processing Script

```python
#!/usr/bin/env python3
"""
Batch process multiple bank statements
"""

import glob
import os
from app import extract_rent_payments, save_rent_payments, read_statement_file

def main():
    # Find all statement files
    statement_files = glob.glob("*_statement.txt")
    
    if not statement_files:
        print("No statement files found!")
        return
    
    all_rent_payments = []
    
    for filepath in statement_files:
        print(f"\n{'='*60}")
        print(f"Processing: {filepath}")
        print('='*60)
        
        statement_text = read_statement_file(filepath)
        if statement_text:
            rent_payments = extract_rent_payments(statement_text)
            all_rent_payments.extend(rent_payments)
            print(f"Found {len(rent_payments)} payment(s)")
    
    # Save all payments
    if all_rent_payments:
        save_rent_payments(all_rent_payments, "all_rent_payments")
        print(f"\nTotal rent payments across all statements: {len(all_rent_payments)}")
    else:
        print("\nNo rent payments found in any statements.")

if __name__ == "__main__":
    main()
```

Save this as `batch_process.py` and run with:
```bash
python batch_process.py
```

## Next Steps

- Add support for PDF bank statements using PyPDF2
- Implement web interface using Streamlit
- Add email integration to process statements automatically
- Create visualizations with matplotlib or plotly
- Export to accounting software formats
