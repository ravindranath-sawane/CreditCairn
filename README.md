# 💳 CreditCairn

An AI-powered Canadian credit card rewards assistant built with Streamlit, Google Gemini, and ChromaDB.

## 🌟 Features

- **Smart Recommendations**: Get personalized credit card suggestions based on your spending patterns
- **RAG-Powered**: Uses Retrieval-Augmented Generation for accurate, context-aware responses
- **Canadian Focus**: Specialized knowledge of Canadian credit cards and rewards programs
- **Chat Interface**: Natural language conversation for easy interaction
- **Free-Tier Friendly**: Optimized to run on Streamlit Cloud with free-tier resources

## 🏗️ Architecture

### Core Components

1. **data_ingestion.py**: Handles credit card data loading and management
   - Modular data structure with type hinting
   - JSON-based storage
   - Sample Canadian credit card dataset

2. **agent_engine.py**: AI agent with retrieval capabilities
   - Google Gemini 1.5 Flash integration
   - ChromaDB vector database for semantic search
   - RAG-based context retrieval
   - Custom tools for card recommendations

3. **app.py**: Streamlit chat interface
   - Interactive chat interface
   - Session state management
   - Real-time AI responses
   - Sidebar configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google API Key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/ravindranath-sawane/CreditCairn.git
cd CreditCairn
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser and navigate to `http://localhost:8501`

### Test Data Ingestion

```bash
python data_ingestion.py
```

### Test Agent Engine

```bash
export GOOGLE_API_KEY='your-api-key-here'
python agent_engine.py
```

## ☁️ Streamlit Cloud Deployment

1. Fork this repository to your GitHub account

2. Go to [Streamlit Cloud](https://streamlit.io/cloud)

3. Click "New app" and select your forked repository

4. Set the main file path to `app.py`

5. In "Advanced settings", add your secrets:
   ```toml
   GOOGLE_API_KEY = "your-api-key-here"
   ```

6. Click "Deploy"!

## 📊 Credit Card Data

The application includes sample data for popular Canadian credit cards:

- Tangerine Money-Back Credit Card
- Scotiabank Gold American Express
- Simplii Financial Cash Back Visa
- BMO Cashback World Elite Mastercard
- TD Aeroplan Visa Infinite
- CIBC Dividend Visa Infinite
- American Express Cobalt Card
- Rogers World Elite Mastercard

## 💡 Usage Examples

Ask questions like:

- "What's the best no-fee cash back card for groceries?"
- "Which card has the best travel rewards?"
- "Compare the Tangerine and Simplii cards"
- "Show me cards with good welcome bonuses"
- "What's the best card for dining rewards?"

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 1.5 Flash
- **Vector Database**: ChromaDB
- **Language**: Python 3.9+
- **Type Hints**: Full type annotation support

## 📁 Project Structure

```
CreditCairn/
├── app.py                  # Streamlit chat interface
├── agent_engine.py         # Gemini agent with RAG
├── data_ingestion.py       # Data loading and management
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── .env.example           # Environment variables template
├── data/                  # Credit card data (auto-generated)
└── .chromadb/            # ChromaDB storage (auto-generated)
```

## 🔒 Environment Variables

- `GOOGLE_API_KEY`: Your Google API key for Gemini access

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Credit card data is for informational purposes only
- Always verify card details with the issuing bank
- Built with love using Streamlit and Google Gemini

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This application provides information for educational purposes only. Always verify credit card details, terms, and conditions with the issuing financial institution before making any financial decisions.