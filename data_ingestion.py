"""
Data ingestion module for scraping Canadian credit card information.
This module provides functionality to collect and store credit card data.
"""

from typing import List, Dict, Optional, Any
import json
import os
from pathlib import Path
from datetime import datetime


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
        self.cards_data: List[CreditCardData] = []
    
    def load_sample_data(self) -> List[CreditCardData]:
        """
        Load sample Canadian credit card data.
        In production, this would scrape from actual sources.
        
        Returns:
            List of credit card data objects
        """
        # Sample data representing Canadian credit cards
        sample_cards = [
            CreditCardData(
                name="Tangerine Money-Back Credit Card",
                issuer="Tangerine Bank",
                annual_fee=0.0,
                rewards_rate="2% in 2 categories, 0.5% on everything else",
                welcome_bonus="$50 cash back or 10% cash back up to $150 in first 3 months",
                categories=["Groceries", "Gas", "Dining", "Transit", "Entertainment"],
                perks=["No annual fee", "No foreign transaction fees", "Mobile device insurance"],
                description="Popular no-fee cash back card offering 2% back in up to 2 categories of your choice and 0.5% on all other purchases.",
            ),
            CreditCardData(
                name="Scotiabank Gold American Express",
                issuer="Scotiabank",
                annual_fee=120.0,
                rewards_rate="5x points on groceries, dining, entertainment; 3x on gas, transit; 1x on everything else",
                welcome_bonus="30,000 bonus points",
                categories=["Groceries", "Dining", "Entertainment", "Gas", "Transit"],
                perks=["Scene+ points", "No foreign transaction fees", "Purchase protection", "Extended warranty"],
                description="Premium rewards card earning 5x Scene+ points on groceries, dining, and entertainment, with no foreign transaction fees.",
            ),
            CreditCardData(
                name="Simplii Financial Cash Back Visa",
                issuer="Simplii Financial",
                annual_fee=0.0,
                rewards_rate="4% on dining, 1.5% on groceries & gas, 0.5% on everything else",
                welcome_bonus="10% cash back up to $100 in first 3 months",
                categories=["Dining", "Groceries", "Gas"],
                perks=["No annual fee", "Contactless payments", "Visa benefits"],
                description="No-fee card offering 4% cash back on dining, 1.5% on groceries and gas stations.",
            ),
            CreditCardData(
                name="BMO Cashback World Elite Mastercard",
                issuer="BMO",
                annual_fee=120.0,
                rewards_rate="5% on groceries, 3% on gas & transit, 1% on everything else",
                welcome_bonus="$400 cash back",
                categories=["Groceries", "Gas", "Transit"],
                perks=["World Elite benefits", "Travel insurance", "Purchase protection", "Lounge access"],
                description="Premium cash back card offering 5% back on groceries, 3% on gas and transit, plus World Elite Mastercard benefits.",
            ),
            CreditCardData(
                name="TD Aeroplan Visa Infinite",
                issuer="TD",
                annual_fee=139.0,
                rewards_rate="1.5 points per $1 on eligible Air Canada purchases, 1 point per $1 on gas, groceries, transit",
                welcome_bonus="20,000 bonus Aeroplan points",
                categories=["Travel", "Gas", "Groceries", "Transit"],
                perks=["Priority check-in", "First bag free", "Travel insurance", "TD Rewards"],
                description="Premium travel card earning Aeroplan points with bonus multipliers on Air Canada purchases and everyday spending.",
            ),
            CreditCardData(
                name="CIBC Dividend Visa Infinite",
                issuer="CIBC",
                annual_fee=120.0,
                rewards_rate="4% on groceries & gas, 2% on transit & restaurants, 1% on everything else",
                welcome_bonus="10% cash back up to $200 in first 4 months",
                categories=["Groceries", "Gas", "Transit", "Dining"],
                perks=["Visa Infinite benefits", "Travel insurance", "Purchase protection"],
                description="Cash back card with accelerated rates on groceries, gas, transit, and dining, plus comprehensive insurance coverage.",
            ),
            CreditCardData(
                name="American Express Cobalt Card",
                issuer="American Express",
                annual_fee=155.88,
                rewards_rate="5x points on groceries & dining, 3x on streaming, 2x on gas & transit, 1x on everything else",
                welcome_bonus="Up to 30,000 bonus points",
                categories=["Groceries", "Dining", "Streaming", "Gas", "Transit"],
                perks=["Amex Offers", "Purchase protection", "Mobile device insurance", "Extended warranty"],
                description="Popular points card with 5x multiplier on eats and drinks, including groceries, restaurants, and bars.",
            ),
            CreditCardData(
                name="Rogers World Elite Mastercard",
                issuer="Rogers Bank",
                annual_fee=0.0,
                rewards_rate="3% on foreign currency transactions, 1.5% on all other purchases",
                welcome_bonus="$50 statement credit",
                categories=["Foreign purchases", "General"],
                perks=["No annual fee", "World Elite benefits", "Travel insurance", "Lounge access"],
                description="No-fee World Elite card offering 3% back on USD purchases, making it ideal for cross-border shopping and travel.",
            ),
        ]
        
        self.cards_data = sample_cards
        return sample_cards
    
    def save_to_json(self, filename: str = "credit_cards.json") -> str:
        """
        Save credit card data to JSON file.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            Path to saved file
        """
        filepath = self.data_dir / filename
        
        data_to_save = {
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "total_cards": len(self.cards_data),
                "source": "Canadian credit card data",
            },
            "cards": [card.to_dict() for card in self.cards_data],
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_from_json(self, filename: str = "credit_cards.json") -> List[CreditCardData]:
        """
        Load credit card data from JSON file.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            List of credit card data objects
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            return []
        
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
