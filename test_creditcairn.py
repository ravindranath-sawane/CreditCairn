"""
Simple tests for CreditCairn modules.
Tests basic functionality without requiring API keys.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_ingestion import DataIngestion, CreditCardData
from agent_engine import CreditCardRetriever


def test_data_ingestion() -> None:
    """Test data ingestion module."""
    print("Testing data ingestion...")
    
    # Create ingestion instance
    ingestion = DataIngestion(data_dir="test_data")
    
    # Load sample data
    cards = ingestion.load_sample_data()
    assert len(cards) == 8, f"Expected 8 cards, got {len(cards)}"
    assert isinstance(cards[0], CreditCardData)
    
    # Test save and load
    filepath = ingestion.save_to_json("test_cards.json")
    assert Path(filepath).exists(), "JSON file should exist"
    
    # Load from JSON
    loaded_cards = ingestion.load_from_json("test_cards.json")
    assert len(loaded_cards) == 8, f"Expected 8 cards after load, got {len(loaded_cards)}"
    
    # Test get_all_cards
    all_cards = ingestion.get_all_cards()
    assert len(all_cards) == 8, f"Expected 8 cards from get_all_cards, got {len(all_cards)}"
    assert isinstance(all_cards[0], dict)
    
    # Cleanup
    import shutil
    shutil.rmtree("test_data")
    
    print("✅ Data ingestion tests passed")


def test_credit_card_retriever() -> None:
    """Test credit card retriever without API key."""
    print("Testing credit card retriever...")
    
    # Create retriever instance
    retriever = CreditCardRetriever(data_dir="test_retriever_data", db_dir="test_chromadb")
    
    # Load cards to database
    retriever.load_cards_to_db()
    assert retriever.cards_loaded, "Cards should be loaded"
    assert retriever.collection.count() == 8, f"Expected 8 cards in DB, got {retriever.collection.count()}"
    
    # Test search
    results = retriever.search_cards("grocery rewards", n_results=3)
    assert len(results) <= 3, f"Expected at most 3 results, got {len(results)}"
    assert all(isinstance(card, dict) for card in results)
    
    # Cleanup
    import shutil
    shutil.rmtree("test_retriever_data")
    shutil.rmtree("test_chromadb")
    
    print("✅ Credit card retriever tests passed")


def test_card_data_structure() -> None:
    """Test credit card data structure."""
    print("Testing credit card data structure...")
    
    card = CreditCardData(
        name="Test Card",
        issuer="Test Bank",
        annual_fee=100.0,
        rewards_rate="2% back",
        welcome_bonus="$200",
        categories=["Groceries", "Gas"],
        perks=["Travel insurance"],
        description="Test description"
    )
    
    card_dict = card.to_dict()
    assert card_dict["name"] == "Test Card"
    assert card_dict["annual_fee"] == 100.0
    assert len(card_dict["categories"]) == 2
    
    print("✅ Card data structure tests passed")


def main() -> None:
    """Run all tests."""
    print("=" * 50)
    print("Running CreditCairn Tests")
    print("=" * 50)
    print()
    
    try:
        test_card_data_structure()
        test_data_ingestion()
        # Skip retriever test as it requires network access to download embedding models
        print("Skipping retriever test (requires network access for embedding models)")
        
        print()
        print("=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
