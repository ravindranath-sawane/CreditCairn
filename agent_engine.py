"""
Agent engine module for CreditCairn using Gemini 1.5 Flash and ChromaDB.
This module provides RAG-based functionality for credit card recommendations.
"""

from typing import List, Dict, Any, Optional, Callable
import os
import json
import time
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
import chromadb
from chromadb.config import Settings
from google import genai
from google.genai import types, errors
from data_ingestion import DataIngestion


class CreditCardRetriever:
    """Handles credit card data retrieval using ChromaDB."""
    
    def __init__(self, data_dir: str = "data", db_dir: str = ".chromadb") -> None:
        """
        Initialize the credit card retriever.
        
        Args:
            data_dir: Directory containing credit card data
            db_dir: Directory for ChromaDB storage
        """
        self.data_dir = Path(data_dir)
        self.db_dir = Path(db_dir)
        
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=str(self.db_dir),
            anonymized_telemetry=False,
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="credit_cards",
            metadata={"description": "Canadian credit card information"}
        )
        
        self.cards_loaded = False
    
    def load_cards_to_db(self, force_reload: bool = False) -> None:
        """
        Load credit card data into ChromaDB.
        
        Args:
            force_reload: Force reload even if data already loaded
        """
        # Check if collection already has data
        if self.collection.count() > 0 and not force_reload:
            self.cards_loaded = True
            return
        
        # Load credit card data
        ingestion = DataIngestion(data_dir=str(self.data_dir))
        
        # Try to load from JSON first, otherwise load sample data
        cards = ingestion.load_from_json()
        if not cards:
            cards = ingestion.load_sample_data()
            ingestion.save_to_json()
        
        # Clear existing data if force reload
        if force_reload and self.collection.count() > 0:
            self.client.delete_collection("credit_cards")
            self.collection = self.client.get_or_create_collection(
                name="credit_cards",
                metadata={"description": "Canadian credit card information"}
            )
        
        # Prepare documents for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for idx, card in enumerate(cards):
            card_dict = card.to_dict()
            
            # Create a rich text representation for embedding
            doc_text = f"""
Card Name: {card_dict['name']}
Issuer: {card_dict['issuer']}
Annual Fee: ${card_dict['annual_fee']}
Rewards Rate: {card_dict['rewards_rate']}
Welcome Bonus: {card_dict['welcome_bonus']}
Categories: {', '.join(card_dict['categories'])}
Perks: {', '.join(card_dict['perks'])}
Description: {card_dict['description']}
            """.strip()
            
            # Convert lists to strings for ChromaDB metadata (it doesn't support list types)
            metadata = {
                "name": card_dict['name'],
                "issuer": card_dict['issuer'],
                "annual_fee": card_dict['annual_fee'],
                "rewards_rate": card_dict['rewards_rate'],
                "welcome_bonus": card_dict['welcome_bonus'],
                "categories": ', '.join(card_dict['categories']),
                "perks": ', '.join(card_dict['perks']),
                "description": card_dict['description'],
            }
            
            documents.append(doc_text)
            metadatas.append(metadata)
            ids.append(f"card_{idx}")
        
        # Add to ChromaDB
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        self.cards_loaded = True
    
    def search_cards(
        self,
        query: str,
        n_results: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant credit cards based on query.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of matching credit cards with metadata
        """
        if not self.cards_loaded:
            self.load_cards_to_db()
        
        # Perform similarity search
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count()),
            where=filters
        )
        
        # Format results
        cards = []
        if results['metadatas'] and len(results['metadatas']) > 0:
            for metadata, distance in zip(results['metadatas'][0], results['distances'][0]):
                card = metadata.copy()
                # Convert string categories back to list
                if 'categories' in card and isinstance(card['categories'], str):
                    card['categories'] = [c.strip() for c in card['categories'].split(',')]
                if 'perks' in card and isinstance(card['perks'], str):
                    card['perks'] = [p.strip() for p in card['perks'].split(',')]
                card['relevance_score'] = 1 - distance  # Convert distance to similarity score
                cards.append(card)
        
        return cards


def is_rate_limit_error(e: Exception) -> bool:
    """Check if exception is a rate limit error."""
    # Check for ClientError (new SDK) or APIError with 429 code
    if isinstance(e, (errors.APIError, errors.ClientError)):
        # Check code attribute safely
        code = getattr(e, 'code', None)
        if code == 429:
            return True
        # Check status_code just in case
        status_code = getattr(e, 'status_code', None)
        if status_code == 429:
            return True
        # Check string representation
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return True
            
    return False


class CreditCairnAgent:
    """Main agent for credit card recommendations using Gemini."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-flash-latest",
        data_dir: str = "data"
    ) -> None:
        """
        Initialize the CreditCairn agent.
        
        Args:
            api_key: Google API key (or set GOOGLE_API_KEY env var)
            model_name: Gemini model to use
            data_dir: Directory containing credit card data
        """
        # Configure Gemini
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        
        self.model_name = model_name
        self.chat = None
        
        # Initialize retriever
        self.retriever = CreditCardRetriever(data_dir=data_dir)
        self.retriever.load_cards_to_db()
        
        # System prompt for the agent
        self.system_prompt = """You are CreditCairn, an expert AI assistant specializing in Canadian credit card rewards optimization.

Your role is to help users:
1. Find the best credit cards based on their spending patterns
2. Maximize rewards and points earnings
3. Understand card benefits and features
4. Compare different credit cards
5. Optimize their credit card strategy

When answering:
- Be friendly, helpful, and clear
- Focus on Canadian credit cards only
- Provide specific recommendations based on user needs
- Explain rewards rates and benefits clearly
- Consider annual fees vs. rewards value
- Highlight welcome bonuses when relevant
- Be honest about card limitations

Always base your recommendations on the credit card data provided to you."""
    
    def start_chat(self) -> None:
        """Start a new chat session."""
        if not self.client:
            if not self.api_key:
                raise ValueError("No API key provided.")
            self.client = genai.Client(api_key=self.api_key)
        
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=2048,
            )
        )
    
    def get_card_context(self, query: str, n_results: int = 3) -> str:
        """
        Retrieve relevant credit card information for the query.
        
        Args:
            query: User query
            n_results: Number of cards to retrieve
            
        Returns:
            Formatted context string
        """
        cards = self.retriever.search_cards(query, n_results=n_results)
        
        if not cards:
            return "No matching credit cards found."
        
        context = "Here are the most relevant credit cards:\n\n"
        
        for idx, card in enumerate(cards, 1):
            context += f"{idx}. {card['name']} ({card['issuer']})\n"
            context += f"   Annual Fee: ${card['annual_fee']}\n"
            context += f"   Rewards: {card['rewards_rate']}\n"
            context += f"   Welcome Bonus: {card['welcome_bonus']}\n"
            context += f"   Categories: {', '.join(card['categories'])}\n"
            context += f"   Key Perks: {', '.join(card['perks'][:3])}\n"
            context += f"   Description: {card['description']}\n\n"
        
        return context
    
    @retry(
        retry=retry_if_exception(is_rate_limit_error),
        wait=wait_exponential(multiplier=2, min=4, max=60),
        stop=stop_after_attempt(5)
    )
    def chat_completion(self, user_message: str) -> str:
        """
        Get a chat completion from the agent.
        
        Args:
            user_message: User's message
            
        Returns:
            Agent's response
        """
        if not self.chat:
            self.start_chat()
        
        # Retrieve relevant card information
        card_context = self.get_card_context(user_message)
        
        # Construct prompt with context
        prompt = f"""{self.system_prompt}

{card_context}

User Question: {user_message}

Please provide a helpful response based on the credit card information provided."""
        
        # Get response from Gemini
        response = self.chat.send_message(prompt)
        
        return response.text
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        """
        Get all available credit cards.
        
        Returns:
            List of all credit cards
        """
        return self.retriever.search_cards("credit card", n_results=100)


def main() -> None:
    """Main function to demonstrate agent functionality."""
    print("🤖 CreditCairn Agent Engine")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n⚠️  Warning: No GOOGLE_API_KEY found in environment.")
        print("The agent requires a Google API key to function.")
        print("Set it using: export GOOGLE_API_KEY='your-api-key'")
        return
    
    # Initialize agent
    print("\n🔧 Initializing agent...")
    agent = CreditCairnAgent()
    
    print("✅ Agent initialized successfully!")
    print(f"📊 Loaded {agent.retriever.collection.count()} credit cards into database")
    
    # Example query
    print("\n💬 Example Query:")
    query = "What's the best no-fee cash back card for groceries?"
    print(f"User: {query}")
    
    try:
        response = agent.chat_completion(query)
        print(f"\n🤖 CreditCairn: {response}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have a valid GOOGLE_API_KEY set.")


if __name__ == "__main__":
    main()
