import openai
import os
import dotenv
import json
from datetime import datetime

# Load environment variables
dotenv.load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("API_KEY")

# Enable below if you use Azure OpenAI
if os.getenv("API_BASE"):
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'
    openai.api_base = os.getenv("API_BASE")


def extract_rent_payments(statement_text):
    """
    Use OpenAI to extract rent payments from bank statement text.
    
    Args:
        statement_text (str): The bank statement text to analyze
        
    Returns:
        list: List of rent payment transactions
    """
    
    prompt = f"""Analyze the following bank statement and extract all rent-related payments.
For each rent payment, identify:
- Date
- Amount
- Payee/Description
- Payment method/reference

Bank Statement:
{statement_text}

Return the results as a JSON array with the following format:
[
  {{
    "date": "YYYY-MM-DD",
    "amount": "amount in currency",
    "payee": "payee name",
    "description": "transaction description",
    "reference": "payment reference if available"
  }}
]

Only include transactions that are clearly rent payments (look for keywords like "rent", "landlord", "housing", "lease", etc.).
"""

    try:
        # Use Azure OpenAI if configured, otherwise use standard OpenAI
        if os.getenv("DEPLOYMENT_NAME"):
            response = openai.ChatCompletion.create(
                engine=os.getenv("DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": "You are a financial assistant that helps analyze bank statements and extract specific transaction types."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial assistant that helps analyze bank statements and extract specific transaction types."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
        
        # Extract the response content
        content = response.choices[0].message.content
        
        # Parse the JSON response
        # Remove markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        rent_payments = json.loads(content)
        return rent_payments
        
    except Exception as e:
        print(f"Error extracting rent payments: {e}")
        return []


def save_rent_payments(rent_payments, output_folder="extracted_rent_payments"):
    """
    Save extracted rent payments to individual files in a folder.
    
    Args:
        rent_payments (list): List of rent payment transactions
        output_folder (str): Folder to save the extracted payments
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
    
    Args:
        filepath (str): Path to the bank statement file
        
    Returns:
        str: Contents of the bank statement
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
    Main function to run the bank statement analyzer.
    """
    print("=== Bank Statement Rent Payment Extractor ===\n")
    
    # Check for sample statement file
    sample_file = "sample_statement.txt"
    
    if os.path.exists(sample_file):
        print(f"📄 Using statement file: {sample_file}\n")
        statement_text = read_statement_file(sample_file)
    else:
        # Use example statement if no file provided
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
        
        # Extract rent payments using AI
        rent_payments = extract_rent_payments(statement_text)
        
        if rent_payments:
            print(f"Found {len(rent_payments)} rent payment(s):\n")
            for i, payment in enumerate(rent_payments, 1):
                print(f"{i}. Date: {payment.get('date', 'N/A')}")
                print(f"   Amount: {payment.get('amount', 'N/A')}")
                print(f"   Payee: {payment.get('payee', 'N/A')}")
                print(f"   Description: {payment.get('description', 'N/A')}\n")
            
            # Save to files
            save_rent_payments(rent_payments)
        else:
            print("No rent payments found in the statement.")
    else:
        print("Unable to process bank statement.")


if __name__ == "__main__":
    main()
