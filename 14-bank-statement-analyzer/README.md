# Bank Statement Rent Payment Extractor

A practical AI-powered application that analyzes bank statements and automatically extracts rent payment transactions into organized files.

## 🎯 What This App Does

This application uses Generative AI (OpenAI's GPT models) to:
1. Analyze bank statement text
2. Identify rent-related payments using natural language understanding
3. Extract key details (date, amount, payee, description)
4. Save each rent payment as a separate JSON file in an organized folder

## 🚀 Getting Started

### Quick Start (No API Key Required!)

Try the demo version first to see how it works:

```bash
cd 14-bank-statement-analyzer
python demo.py
```

This will run a demonstration using keyword-based extraction on the sample bank statement.

### Full Version Setup

For the AI-powered version:

#### Prerequisites

- Python 3.7 or higher
- OpenAI API key (or Azure OpenAI credentials)
- Required Python packages (see requirements in main repo)

#### Installation

1. Navigate to this directory:
```bash
cd 14-bank-statement-analyzer
```

2. Install required packages:
```bash
pip install openai python-dotenv
```

3. Set up your environment variables by creating a `.env` file:
```bash
# For Standard OpenAI
API_KEY=your_openai_api_key_here

# For Azure OpenAI (optional)
API_BASE=your_azure_endpoint
DEPLOYMENT_NAME=your_deployment_name
```

### Usage

#### Option 1: Demo Mode (No API Key)

Run the demo version to test without an API key:

```bash
python demo.py
```

#### Option 2: AI-Powered Version

Run the full AI-powered application:

```bash
python app.py
```

This will analyze the `sample_statement.txt` file and extract rent payments using OpenAI.

#### Option 3: Using Your Own Bank Statement

1. Create a text file with your bank statement content (you can copy/paste from a PDF or export)
2. Save it as `sample_statement.txt` in this directory (or modify the code to point to your file)
3. Run the application:

```bash
python app.py  # or python demo.py for keyword-based extraction
```

## 📂 Output

The application creates an `extracted_rent_payments` folder containing:

1. **rent_payments_summary.json** - A summary file with all rent payments
2. **Individual payment files** - One JSON file per rent payment (e.g., `rent_payment_20240105_1.json`)

### Example Output

```json
{
  "date": "2024-01-05",
  "amount": "-1,850.00",
  "payee": "RIVERSIDE APARTMENTS",
  "description": "RENT - RIVERSIDE APARTMENTS",
  "reference": "Monthly rent payment"
}
```

## 🧠 How It Works

This application demonstrates practical use of Generative AI for document analysis:

1. **Prompt Engineering**: The app uses a carefully crafted prompt that instructs the AI to:
   - Identify rent-related keywords ("rent", "landlord", "housing", "lease")
   - Extract structured data from unstructured text
   - Return results in a specific JSON format

2. **Natural Language Understanding**: The AI model understands context and can identify rent payments even when they're described differently:
   - "RENT - RIVERSIDE APARTMENTS"
   - "LANDLORD PAYMENT - JAN RENT"
   - "HOUSING LEASE PMT - UNIT 4B"

3. **Structured Output**: The AI converts natural language transactions into structured JSON data that can be easily processed by other applications.

## 🎓 Learning Objectives

This example teaches you:
- How to use OpenAI's API for document analysis
- Prompt engineering for data extraction tasks
- Handling JSON responses from AI models
- File I/O operations in Python
- Practical AI application development

## 🔧 Customization

You can easily modify this app to extract other types of transactions:

1. **Extract Utility Payments**: Change the prompt to look for "utility", "electric", "gas", "water"
2. **Extract Grocery Expenses**: Look for "grocery", "supermarket", "food"
3. **Extract Subscriptions**: Look for "subscription", "monthly", "recurring"

Simply update the prompt in the `extract_rent_payments()` function!

## 🛡️ Privacy & Security

**Important**: This app processes financial data. Best practices:
- Never commit real bank statements to version control
- Use `.gitignore` to exclude sensitive files
- Consider anonymizing data before processing
- Keep your API keys secure in `.env` files
- Delete extracted files when no longer needed

## 📝 File Structure

```
14-bank-statement-analyzer/
├── app.py                      # Main AI-powered application
├── demo.py                     # Demo version (no API key needed)
├── sample_statement.txt        # Sample bank statement
├── README.md                   # This file
├── .env.example               # Environment variable template
└── extracted_rent_payments/   # Output folder (created automatically)
    ├── rent_payments_summary.json
    └── rent_payment_*.json
```

## 🤝 Contributing

Feel free to enhance this application by:
- Adding support for different statement formats (CSV, PDF)
- Implementing date range filters
- Adding export to Excel/CSV functionality
- Improving rent payment detection accuracy

## 📚 Related Lessons

This app builds on concepts from:
- Lesson 6: Text Generation Apps
- Lesson 7: Building Chat Applications
- Lesson 11: Integrating with Function Calling

## ⚠️ Troubleshooting

**Issue**: "No module named 'openai'"
- **Solution**: Install dependencies: `pip install -r requirements.txt` (from repo root)

**Issue**: "API key not found"
- **Solution**: Make sure you have created a `.env` file with your API key

**Issue**: "No rent payments found"
- **Solution**: The AI might not recognize rent payments in your statement format. Try adjusting the prompt to include specific keywords from your statement.

## 🎉 Example Output

When you run the app, you'll see:

```
=== Bank Statement Rent Payment Extractor ===

📄 Using statement file: sample_statement.txt

🔍 Analyzing statement for rent payments...

Found 3 rent payment(s):

1. Date: 2024-01-05
   Amount: $1,850.00
   Payee: RIVERSIDE APARTMENTS
   Description: RENT - RIVERSIDE APARTMENTS

2. Date: 2024-01-17
   Amount: $1,850.00
   Payee: Landlord
   Description: LANDLORD PAYMENT - JAN RENT

3. Date: 2024-01-28
   Amount: $1,850.00
   Payee: Housing Management
   Description: HOUSING LEASE PMT - UNIT 4B

✅ Summary saved to: extracted_rent_payments/rent_payments_summary.json
   - rent_payment_20240105_1.json
   - rent_payment_20240117_2.json
   - rent_payment_20240128_3.json

📁 Total 3 rent payment(s) extracted to 'extracted_rent_payments' folder
```

## 📄 License

This project is part of the Generative AI for Beginners course and follows the same MIT license.
