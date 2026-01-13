"""
Data ingestion module for scraping Canadian credit card information.
This module provides functionality to collect and store credit card data.
"""

from typing import List, Dict, Optional, Any
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import logging
from scraper import CreditCardScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreditCardData:
    """Model for credit card data structure."""
    
    def __init__(
        self,
        name: str,
        issuer: str,
        annual_fee: float,
        rewards_rate: str,
        welcome_bonus: str,
        categories: List[str],
        perks: List[str],
        description: str,
    ) -> None:
        self.name = name
        self.issuer = issuer
        self.annual_fee = annual_fee
        self.rewards_rate = rewards_rate
        self.welcome_bonus = welcome_bonus
        self.categories = categories
        self.perks = perks
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert credit card data to dictionary."""
        return {
            "name": self.name,
            "issuer": self.issuer,
            "annual_fee": self.annual_fee,
            "rewards_rate": self.rewards_rate,
            "welcome_bonus": self.welcome_bonus,
            "categories": self.categories,
            "perks": self.perks,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreditCardData':
        """Create CreditCardData from dictionary."""
        return cls(
            name=data.get("name", "Unknown Card"),
            issuer=data.get("issuer", "Unknown Issuer"),
            annual_fee=float(data.get("annual_fee", 0.0)),
            rewards_rate=data.get("rewards_rate", ""),
            welcome_bonus=data.get("welcome_bonus", ""),
            categories=data.get("categories", []),
            perks=data.get("perks", []),
            description=data.get("description", "")
        )


class DataIngestion:
    """Handles credit card data ingestion and storage."""
    
    def __init__(self, data_dir: str = "data") -> None:
        """
        Initialize data ingestion handler.
        
        Args:
            data_dir: Directory to store scraped data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.data_file = self.data_dir / "credit_cards.json"
        self.metadata_file = self.data_dir / "metadata.json"
        self.cards_data: List[CreditCardData] = []
        
    def needs_update(self) -> bool:
        """Check if data needs to be updated (older than 1 week)."""
        if not self.data_file.exists() or not self.metadata_file.exists():
            return True
            
        try:
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
                last_updated = datetime.fromisoformat(metadata['last_updated'])
                # Check if older than 7 days
                if datetime.now() - last_updated > timedelta(days=7):
                    logger.info("Data is older than 7 days, update required.")
                    return True
                return False
        except (json.JSONDecodeError, KeyError, ValueError):
            return True

    def update_data(self) -> List[CreditCardData]:
        """
        Fetching latest data using Scraper.
        """
        logger.info("Starting data update process...")
        scraper = CreditCardScraper()
        raw_cards = scraper.fetch_current_cards()
        
        # Convert to CreditCardData objects
        self.cards_data = [CreditCardData.from_dict(card) for card in raw_cards]
        
        # Save to disk
        self.save_to_json()
        
        # Update metadata
        with open(self.metadata_file, 'w') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'source': 'scraper',
                'count': len(self.cards_data)
            }, f, indent=2)
            
        logger.info(f"Updated database with {len(self.cards_data)} cards.")
        return self.cards_data
    
    def load_from_json(self) -> Optional[List[CreditCardData]]:
        """Load credit card data from JSON file."""
        if self.needs_update():
            return self.update_data()
            
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.cards_data = [CreditCardData.from_dict(item) for item in data]
                return self.cards_data
            except json.JSONDecodeError:
                logger.error("Error reading data file, forcing update.")
                return self.update_data()
        return None

    def save_to_json(self) -> None:
        """Save scraped data to JSON file."""
        data = [card.to_dict() for card in self.cards_data]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_sample_data(self) -> List[CreditCardData]:
        """Legacy method maintained for compatibility."""
        return self.update_data()


    # End of class

        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.cards_data = [
            CreditCardData(**card_data) for card_data in data.get("cards", [])
        ]
        
        return self.cards_data
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        """
        Get all credit card data as dictionaries.
        
        Returns:
            List of credit card dictionaries
        """
        return [card.to_dict() for card in self.cards_data]


def main() -> None:
    """Main function to demonstrate data ingestion."""
    print("🏦 CreditCairn Data Ingestion")
    print("=" * 50)
    
    # Initialize data ingestion
    ingestion = DataIngestion()
    
    # Load sample data
    print("\n📥 Loading sample Canadian credit card data...")
    cards = ingestion.load_sample_data()
    print(f"✅ Loaded {len(cards)} credit cards")
    
    # Save to JSON
    print("\n💾 Saving data to JSON...")
    filepath = ingestion.save_to_json()
    print(f"✅ Data saved to: {filepath}")
    
    # Display summary
    print("\n📊 Summary:")
    for card in cards:
        print(f"  • {card.name} ({card.issuer}) - ${card.annual_fee}/year")


if __name__ == "__main__":
    main()
