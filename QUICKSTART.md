# CreditCairn Quick Start

## 🚀 Get Started in 3 Steps

### 1. Get a Google API Key
Visit [Google AI Studio](https://makersuite.google.com/app/apikey) and create a free API key.

### 2. Set Your API Key
**Option A: Environment Variable**
```bash
export GOOGLE_API_KEY='your-api-key-here'
```

**Option B: In the Streamlit App**
Enter your API key in the sidebar when the app starts.

### 3. Run the App
```bash
streamlit run app.py
```

## 💡 Example Questions

Try asking CreditCairn:

- "What's the best no-fee card for groceries?"
- "Which card has the best travel rewards?"
- "Show me cards with good welcome bonuses under $150 annual fee"
- "Compare the Tangerine and Simplii cash back cards"
- "What card should I get if I spend a lot on dining?"
- "Are there any cards with no foreign transaction fees?"

## 📚 Available Cards

CreditCairn knows about these popular Canadian credit cards:

| Card | Annual Fee | Best For |
|------|------------|----------|
| Tangerine Money-Back | $0 | 2% in 2 categories |
| Simplii Cash Back Visa | $0 | 4% on dining |
| Rogers World Elite | $0 | 3% on USD purchases |
| Scotiabank Gold Amex | $120 | 5x points groceries/dining |
| BMO Cashback World Elite | $120 | 5% on groceries |
| TD Aeroplan Visa Infinite | $139 | Travel rewards |
| CIBC Dividend Visa Infinite | $120 | 4% groceries & gas |
| Amex Cobalt | $155.88 | 5x points eats & drinks |

## 🎯 Use Cases

### For Students/Budget-Conscious
Ask about: "no-fee cards with good rewards"

### For Frequent Travelers
Ask about: "travel rewards and points cards"

### For Grocery Shopping
Ask about: "best grocery rewards cards"

### For Dining Out
Ask about: "dining and restaurant cash back"

### For Gas Purchases
Ask about: "best cards for gas stations"

## 🔧 Troubleshooting

### "No API key found"
- Make sure you've set `GOOGLE_API_KEY` environment variable
- Or enter it manually in the sidebar

### "Import errors"
```bash
pip install -r requirements.txt
```

### "ChromaDB errors"
- First run requires internet to download embedding model
- Database will be created in `.chromadb/` directory

## 📖 Learn More

- **README.md** - Full documentation
- **DEPLOYMENT.md** - Deployment guide for Streamlit Cloud
- **data_ingestion.py** - View credit card data structure

## 🆘 Support

Having issues? Check:
1. Your API key is valid
2. All dependencies are installed
3. Python version is 3.9 or higher

## 🎉 Features

✅ Natural language queries
✅ Context-aware recommendations
✅ Card comparisons
✅ Rewards optimization tips
✅ Welcome bonus information
✅ No-fee options
✅ Premium card benefits

---

**Happy optimizing your credit card rewards! 💳✨**
