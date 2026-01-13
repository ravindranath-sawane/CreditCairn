# Deployment Guide for CreditCairn

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account with repository access
- Google API Key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Steps

1. **Fork or Push Repository**
   - Ensure your code is pushed to GitHub
   - Repository should be public or you should have Streamlit Cloud access

2. **Sign in to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Create New App**
   - Click "New app"
   - Select your repository: `ravindranath-sawane/CreditCairn`
   - Branch: `main` (or your preferred branch)
   - Main file path: `app.py`

4. **Configure Secrets**
   - Click "Advanced settings"
   - In the "Secrets" section, add:
   ```toml
   GOOGLE_API_KEY = "your-actual-api-key-here"
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for the app to build and start
   - Your app will be available at: `https://[your-app-name].streamlit.app`

### Troubleshooting

#### Import Errors
- Ensure all dependencies in `requirements.txt` are correct
- Check that Python version is 3.9+

#### API Key Issues
- Verify the API key is correctly set in Secrets
- Test the key manually at [Google AI Studio](https://aistudio.google.com/)

#### ChromaDB Issues
- ChromaDB will create its database locally on first run
- The database persists between restarts on Streamlit Cloud

#### Memory Issues
- Streamlit Cloud free tier has 1GB RAM limit
- ChromaDB uses local embeddings (no external service needed)
- Sample data is small enough for free tier

## Local Development

### Setup
```bash
# Clone the repository
git clone https://github.com/ravindranath-sawane/CreditCairn.git
cd CreditCairn

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GOOGLE_API_KEY='your-api-key-here'
# On Windows: set GOOGLE_API_KEY=your-api-key-here

# Run the app
streamlit run app.py
```

### Development with .env file
```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your API key
# Then run with python-dotenv
pip install python-dotenv
streamlit run app.py
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google API key for Gemini access |

## File Structure for Deployment

Required files for Streamlit Cloud:
- `app.py` - Main Streamlit application
- `agent_engine.py` - AI agent logic
- `data_ingestion.py` - Data management
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration

## Performance Considerations

### Free Tier Limits
- **RAM**: 1GB (sufficient for this app)
- **Storage**: ChromaDB database stored locally
- **CPU**: Shared resources
- **Bandwidth**: Limited to free tier quotas

### Optimization Tips
1. ChromaDB uses local embeddings (no external API calls)
2. Sample dataset is small (~8 cards)
3. Gemini 1.5 Flash is fast and efficient
4. Streamlit caching helps reduce redundant operations

## Monitoring

### Check App Health
- Use Streamlit Cloud dashboard to view logs
- Monitor app metrics in the dashboard
- Check for errors in the runtime logs

### Common Issues
1. **Slow responses**: Usually due to Gemini API latency
2. **Memory errors**: Restart the app from dashboard
3. **Database errors**: ChromaDB initialization (usually resolves on restart)

## Updating the App

### Automatic Deployment
- Push changes to GitHub
- Streamlit Cloud auto-deploys on push to main branch
- Monitor deployment status in dashboard

### Manual Reboot
- Use "Reboot app" button in Streamlit Cloud dashboard
- Useful after changing secrets or configuration

## Support

For issues:
1. Check [Streamlit Community Forums](https://discuss.streamlit.io/)
2. Check [Google AI Documentation](https://ai.google.dev/docs)
3. Open an issue on GitHub repository
