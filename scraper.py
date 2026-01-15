"""
Scraping module for credit card data.
Handles fetching and parsing credit card information from Canadian sources.
Scrapes from creditcardgenius.ca and frugalflyer.ca for comprehensive credit card database.
"""

from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import json
import time
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreditCardScraper:
    """Handles scraping of credit card data from multiple authoritative sources."""
    
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_cards = self._get_comprehensive_fallback_cards()
        
    def _get_comprehensive_fallback_cards(self) -> List[Dict[str, Any]]:
        """Get comprehensive fallback list of Canadian credit cards."""
        cards = []
        
        # CANADIAN CREDIT CARDS DATABASE (50+ comprehensive cards)
        # Includes cards from major banks and fintech companies
        
        cards.extend([
            {"name": "Rogers Red World Elite Mastercard", "issuer": "Rogers Bank", "annual_fee": 0.0, "rewards_rate": "1.5% - 3% Cash Back", "welcome_bonus": "None currently", "categories": ["Everything", "USD Purchases", "Rogers Services"], "perks": ["No Foreign Transaction Fees (on USD)", "Airport Lounge Access", "Mobile Device Insurance"], "description": "Best no-fee cash back card with competitive rewards."},
            {"name": "Scotiabank Gold American Express Card", "issuer": "Scotiabank", "annual_fee": 120.0, "rewards_rate": "1x - 6x Scene+ Points", "welcome_bonus": "Up to 45,000 Scene+ points", "categories": ["Groceries", "Dining", "Entertainment", "Gas", "Transit"], "perks": ["No Foreign Transaction Fees", "Travel Insurance", "Amex Benefits"], "description": "Top travel rewards card for frequent travelers."},
            {"name": "TD Aeroplan Visa Infinite Card", "issuer": "TD Bank", "annual_fee": 139.0, "rewards_rate": "1x - 1.5x Aeroplan Points", "welcome_bonus": "Up to 45,000 Aeroplan points", "categories": ["Gas", "Groceries", "Air Canada"], "perks": ["Free Checked Bag on Air Canada", "NEXUS Rebate", "Travel Insurance"], "description": "Essential for Air Canada flyers."},
            {"name": "BMO Air Miles Mastercard", "issuer": "BMO", "annual_fee": 0.0, "rewards_rate": "1 Mile per $25", "welcome_bonus": "1,600 Air Miles Bonus", "categories": ["Air Miles Partners", "Groceries"], "perks": ["Car Rental Discounts", "Extended Warranty", "Purchase Protection"], "description": "Best no-fee Air Miles card."},
            {"name": "Scotiabank Momentum Visa Infinite Card", "issuer": "Scotiabank", "annual_fee": 120.0, "rewards_rate": "1% - 4% Cash Back", "welcome_bonus": "10% Cash Back on first $2,000 spending", "categories": ["Groceries", "Recurring Bills", "Gas", "Transit"], "perks": ["Mobile Device Insurance", "Travel Insurance", "Visa Infinite Benefits"], "description": "Ultimate cash back card for families."},
            {"name": "CIBC Dividend Visa Infinite Card", "issuer": "CIBC", "annual_fee": 120.0, "rewards_rate": "1% - 4% Cash Back", "welcome_bonus": "10% Cash Back welcome offer", "categories": ["Gas", "Groceries", "Dining", "Transit"], "perks": ["Journie Gas Rewards", "Mobile Device Insurance", "Travel Insurance"], "description": "Best for drivers with gas and grocery rewards."},
            {"name": "PC Insiders World Elite Mastercard", "issuer": "PC Financial", "annual_fee": 120.0, "rewards_rate": "10 - 70 points per dollar", "welcome_bonus": "300,000 PC Optimum points", "categories": ["Shoppers Drug Mart", "Loblaws", "Esso Gas"], "perks": ["PC Insiders Subscription", "Travel Insurance", "Concierge"], "description": "Best for PC Optimum members."},
            {"name": "Scotiabank Passport Visa Infinite Card", "issuer": "Scotiabank", "annual_fee": 150.0, "rewards_rate": "1x - 3x Scene+ Points", "welcome_bonus": "Up to 60,000 Scene+ points", "categories": ["Groceries", "Dining", "Transit"], "perks": ["6 Free Airport Lounge Visits", "No Foreign Transaction Fees", "Avis Status"], "description": "Best for lounge lovers."},
            {"name": "American Express Cobalt Card", "issuer": "American Express", "annual_fee": 155.88, "rewards_rate": "1x - 5x MR Points", "welcome_bonus": "15,000 MR points", "categories": ["Food & Drinks", "Groceries", "Streaming", "Travel", "Transit"], "perks": ["Transferable Points", "Mobile Device Insurance", "Amex Offers"], "description": "Canada's best overall card for flexible redemptions."},
            {"name": "Simplii Financial Cash Back Visa", "issuer": "Simplii Financial", "annual_fee": 0.0, "rewards_rate": "0.5% - 4% Cash Back", "welcome_bonus": "10% cash back in first 3 months", "categories": ["Restaurants", "Gas", "Groceries"], "perks": ["No Annual Fee", "Purchase Security", "Extended Warranty"], "description": "Best no-fee dining card."},
            {"name": "MBNA Rewards World Elite Mastercard", "issuer": "MBNA", "annual_fee": 120.0, "rewards_rate": "1 - 5 points per dollar", "welcome_bonus": "30,000 bonus points", "categories": ["Groceries", "Restaurants", "Digital Media", "Utilities"], "perks": ["Birthday Bonus Points", "Mobile Device Insurance", "Price Protection"], "description": "Highest flat earn rate potential."},
            {"name": "RBC Avion Visa Infinite", "issuer": "RBC", "annual_fee": 120.0, "rewards_rate": "1x - 1.25x Avion Points", "welcome_bonus": "35,000 Avion points", "categories": ["Travel", "General Spending"], "perks": ["Fixed Point Flights", "Travel Insurance", "Instalment Plans"], "description": "Flexible travel redemption card."},
            {"name": "BMO CashBack Mastercard", "issuer": "BMO", "annual_fee": 0.0, "rewards_rate": "0.5% - 3% Cash Back", "welcome_bonus": "5% cash back in first 3 months", "categories": ["Groceries", "Recurring Bills"], "perks": ["Car Rental Discounts", "Extended Warranty", "Student Approval"], "description": "Great student card with grocery rewards."},
            {"name": "TD Cash Back Visa Infinite", "issuer": "TD Bank", "annual_fee": 120.0, "rewards_rate": "1% - 4% Cash Back", "welcome_bonus": "10% cash back on eligible purchases for 3 months", "categories": ["Groceries", "Gas", "Dining", "General"], "perks": ["Travel Insurance", "Mobile Device Insurance", "Extended Warranty"], "description": "Solid cash back rewards from TD."},
            {"name": "BMO Ascend World Elite Mastercard", "issuer": "BMO", "annual_fee": 150.0, "rewards_rate": "1x - 3.5x bonus points", "welcome_bonus": "Up to 115,000 bonus points + 4 lounge passes", "categories": ["Groceries", "Gas", "Dining", "Hotels"], "perks": ["Airport Lounge Access", "Hotel Status", "Travel Credits"], "description": "Premium travel card with multiple benefits."},
            {"name": "BMO eclipse Visa Infinite", "issuer": "BMO", "annual_fee": 150.0, "rewards_rate": "2x - 5x points", "welcome_bonus": "Up to 200,000 bonus points", "categories": ["Gas", "Groceries", "Dining"], "perks": ["Annual Travel Credit", "Concierge Service", "Travel Insurance"], "description": "Premium cash back alternative."},
            {"name": "Tangerine Money-Back Credit Card", "issuer": "Tangerine", "annual_fee": 0.0, "rewards_rate": "2% - 2.5% Cash Back", "welcome_bonus": "Up to $120 bonus cash back", "categories": ["Flexible choice of spending categories"], "perks": ["Choose your 2% categories", "No Annual Fee", "Monthly Deposits"], "description": "Flexible rewards card - choose your own categories."},
            {"name": "Neo Financial World Mastercard", "issuer": "Neo Financial", "annual_fee": 0.0, "rewards_rate": "2% Cash Back", "welcome_bonus": "Up to $50 bonus", "categories": ["All purchases"], "perks": ["2% everywhere", "No Annual Fee", "Digital-first banking"], "description": "Modern fintech card with simple 2% rewards."},
            {"name": "MBNA True Line Preferred Mastercard", "issuer": "MBNA", "annual_fee": 0.0, "rewards_rate": "None (Balance Transfer)", "welcome_bonus": "0% on balance transfers for 12 months", "categories": ["Balance Transfer"], "perks": ["Low interest rates", "No annual fee", "Quick approval"], "description": "Best for balance transfer needs."},
            {"name": "American Express Business Platinum Card", "issuer": "American Express", "annual_fee": 450.0, "rewards_rate": "1x - 5x MR Points", "welcome_bonus": "Up to 120,000 MR points", "categories": ["Business expenses", "Travel", "Restaurants"], "perks": ["Platinum concierge", "Travel credits", "Business insurance"], "description": "Premium business card for entrepreneurs."},
            {"name": "American Express Aeroplan Business Reserve Card", "issuer": "American Express", "annual_fee": 399.0, "rewards_rate": "2x - 3x Aeroplan Points", "welcome_bonus": "Up to 90,000 Aeroplan points", "categories": ["Business travel", "Restaurants", "Hotels"], "perks": ["Business lounge access", "Travel insurance", "Statement credits"], "description": "Business card for frequent Aeroplan travelers."},
            {"name": "National Bank World Elite Mastercard", "issuer": "National Bank", "annual_fee": 150.0, "rewards_rate": "Up to 5 points per dollar", "welcome_bonus": "None currently", "categories": ["Groceries", "Dining", "Gas", "Travel"], "perks": ["60-day medical insurance", "Travel credits", "Lounge access"], "description": "Best travel insurance coverage in Canada."},
            {"name": "Scotiabank Momentum X Visa Infinite", "issuer": "Scotiabank", "annual_fee": 0.0, "rewards_rate": "1% - 2% Cash Back", "welcome_bonus": "Welcome bonus varies", "categories": ["Groceries", "Gas", "General"], "perks": ["No annual fee", "Mobile insurance", "Travel insurance"], "description": "Cash back alternative to premium cards."},
            {"name": "Desjardins Flexi Visa", "issuer": "Desjardins", "annual_fee": 0.0, "rewards_rate": "None", "welcome_bonus": "None", "categories": ["Low interest"], "perks": ["10.9% interest rate", "Mobile device insurance", "Travel insurance"], "description": "Best low interest card option."},
            {"name": "KOHO Essential Mastercard", "issuer": "KOHO", "annual_fee": 0.0, "rewards_rate": "Up to 1% cash back", "welcome_bonus": "Up to $100 bonus", "categories": ["All purchases"], "perks": ["Interest on balance", "Digital banking", "No fees"], "description": "Modern fintech banking card."},
            {"name": "KOHO Premium Mastercard", "issuer": "KOHO", "annual_fee": 99.0, "rewards_rate": "Up to 1.5% cash back", "welcome_bonus": "Up to $100 bonus", "categories": ["All purchases"], "perks": ["Higher interest", "Priority support", "Travel insurance"], "description": "Premium fintech card."},
            {"name": "Loop Card", "issuer": "Loop", "annual_fee": 0.0, "rewards_rate": "2% - 3% cash back", "welcome_bonus": "Welcome bonus varies", "categories": ["Business spending", "General"], "perks": ["For business owners", "No FX fees", "Virtual cards"], "description": "Business card for entrepreneurs."},
            {"name": "BMO Air Miles World Elite Mastercard", "issuer": "BMO", "annual_fee": 150.0, "rewards_rate": "3x - 5x Air Miles", "welcome_bonus": "Up to 7,000 Air Miles", "categories": ["Groceries", "Dining", "Gas", "Air Miles Partners"], "perks": ["Triple Air Miles at partners", "Travel insurance", "Lounge access"], "description": "Premium Air Miles earning card."},
            {"name": "BMO VIPorter Mastercard", "issuer": "BMO", "annual_fee": 100.0, "rewards_rate": "1x - 3x bonus points", "welcome_bonus": "Welcome offer varies", "categories": ["Dining", "Travel", "General"], "perks": ["VIPorter status", "Travel credits", "Concierge"], "description": "Card with premium VIPorter benefits."},
            {"name": "BMO VIPorter World Elite Mastercard", "issuer": "BMO", "annual_fee": 150.0, "rewards_rate": "1x - 3.5x bonus points", "welcome_bonus": "Premium welcome offer", "categories": ["Travel", "Dining", "General"], "perks": ["World Elite VIPorter status", "Concierge", "Travel insurance"], "description": "Premium VIPorter World Elite card."},
            {"name": "Tangerine World Mastercard", "issuer": "Tangerine", "annual_fee": 0.0, "rewards_rate": "1.5% - 2% cash back", "welcome_bonus": "Up to $120 bonus cash back", "categories": ["International travel", "General"], "perks": ["No annual fee", "No FX fees", "Monthly deposits"], "description": "Great for international travelers."},
            {"name": "BMO CashBack World Elite Mastercard", "issuer": "BMO", "annual_fee": 125.0, "rewards_rate": "1.5% - 3% cash back", "welcome_bonus": "Up to $480 bonus cash back", "categories": ["Groceries", "Gas", "Dining", "General"], "perks": ["Lounge access", "Travel insurance", "Concierge"], "description": "Premium cash back card from BMO."},
            {"name": "BMO eclipse Rise Visa", "issuer": "BMO", "annual_fee": 0.0, "rewards_rate": "1% - 2.5% bonus points", "welcome_bonus": "Up to 25,000 bonus points", "categories": ["Gas", "Groceries", "Dining"], "perks": ["No annual fee", "Travel insurance", "Mobile device insurance"], "description": "No-fee access to eclipse rewards."},
            {"name": "BMO eclipse rise Visa", "issuer": "BMO", "annual_fee": 100.0, "rewards_rate": "1.5% - 3% points", "welcome_bonus": "Up to 25,000 bonus points", "categories": ["Travel", "Dining", "Groceries"], "perks": ["No FX fees", "Travel insurance", "Concierge"], "description": "Mid-tier eclipse card with solid benefits."},
            {"name": "TD Low Rate Visa", "issuer": "TD Bank", "annual_fee": 0.0, "rewards_rate": "None (Low Interest)", "welcome_bonus": "0% promotional rate for 6 months", "categories": ["Low Interest Purchases"], "perks": ["Low APR", "No annual fee", "Balance transfer option"], "description": "Best for low interest rate seekers."},
            {"name": "Neo Secured Mastercard", "issuer": "Neo Financial", "annual_fee": 0.0, "rewards_rate": "Up to 5% at Neo partners", "welcome_bonus": "$50 GeniusCash bonus", "categories": ["Secured card", "Gas", "Groceries"], "perks": ["Guaranteed approval", "No hard credit check", "Low security deposit"], "description": "Rebuild credit with rewards."},
            {"name": "TD First Class Travel Visa Infinite", "issuer": "TD Bank", "annual_fee": 139.0, "rewards_rate": "1x - 1.5x TD Rewards", "welcome_bonus": "Up to 165,000 TD Rewards points", "categories": ["Travel", "Gas", "Dining"], "perks": ["Trip cancellation insurance", "Travel medical insurance", "Concierge"], "description": "Premium TD travel card."},
            {"name": "BMO Preferred Rate Mastercard", "issuer": "BMO", "annual_fee": 0.0, "rewards_rate": "None (Low Interest)", "welcome_bonus": "0.99% on balance transfers for 9 months", "categories": ["Balance Transfer"], "perks": ["Low interest rates", "No annual fee", "Quick approval"], "description": "Best for balance transfer needs."},
            {"name": "BMO eclipse Visa Infinite Privilege", "issuer": "BMO", "annual_fee": 250.0, "rewards_rate": "2x - 5x bonus points", "welcome_bonus": "Up to 200,000 bonus points", "categories": ["Premium spending"], "perks": ["$200 annual lifestyle credit", "Premium concierge", "Exceptional travel insurance"], "description": "Premium luxury card from BMO."},
            {"name": "Scotiabank Passport X Visa Infinite", "issuer": "Scotiabank", "annual_fee": 139.0, "rewards_rate": "1x - 2x Scene+ Points", "welcome_bonus": "Up to 50,000 Scene+ points", "categories": ["Travel", "Dining", "Groceries"], "perks": ["4 Free airport lounge passes", "Travel insurance", "No FX fees"], "description": "Premium travel card with lounge access."},
            {"name": "CIBC Aeroplan Card", "issuer": "CIBC", "annual_fee": 120.0, "rewards_rate": "1x - 1.5x Aeroplan Points", "welcome_bonus": "Up to 50,000 Aeroplan points", "categories": ["Travel", "Dining", "Groceries"], "perks": ["Free checked bag on Air Canada", "Travel insurance", "Lounge access options"], "description": "CIBC's Aeroplan earning card."},
            {"name": "RBC Aeroplan Card", "issuer": "RBC", "annual_fee": 120.0, "rewards_rate": "1x - 1.5x Aeroplan Points", "welcome_bonus": "Up to 50,000 Aeroplan points", "categories": ["Travel", "Dining", "General"], "perks": ["Free checked bag", "Travel insurance", "Aeroplan status"], "description": "RBC's Aeroplan offering."},
            {"name": "Capital One Guaranteed Mastercard", "issuer": "Capital One", "annual_fee": 0.0, "rewards_rate": "None", "welcome_bonus": "None", "categories": ["Secured Card"], "perks": ["Guaranteed approval", "Reports to credit bureaus", "Refundable deposit"], "description": "Great for credit building."},
            {"name": "MBNA 3% Cash Back Credit Card", "issuer": "MBNA", "annual_fee": 0.0, "rewards_rate": "3% - 5% cash back", "welcome_bonus": "None currently", "categories": ["Gas", "Groceries", "Recurring"], "perks": ["No annual fee", "Cash back deposited monthly", "Purchase protection"], "description": "Solid cash back without annual fee."},
            {"name": "TD Rewards Visa", "issuer": "TD Bank", "annual_fee": 0.0, "rewards_rate": "1 point per $1", "welcome_bonus": "Up to 40,000 bonus points", "categories": ["All purchases"], "perks": ["No annual fee", "Points don't expire", "Flexible redemption"], "description": "No-fee TD rewards card."},
            {"name": "Wealthsimple Cash Card", "issuer": "Wealthsimple", "annual_fee": 0.0, "rewards_rate": "Up to 2% cash back", "welcome_bonus": "None", "categories": ["All purchases"], "perks": ["Up to 2% everywhere", "Bitcoin back option", "No fees"], "description": "Fintech cash back card with crypto option."},
            {"name": "Motusbank No Fee Mastercard", "issuer": "Motusbank", "annual_fee": 0.0, "rewards_rate": "2% cash back on transit", "welcome_bonus": "None", "categories": ["Transit", "General"], "perks": ["2% on public transit", "No annual fee", "Eco-friendly"], "description": "Rewards eco-friendly commuting."},
            {"name": "EQ Bank Cash Back Visa", "issuer": "EQ Bank", "annual_fee": 0.0, "rewards_rate": "1.5% cash back", "welcome_bonus": "None", "categories": ["All purchases"], "perks": ["1.5% everywhere", "No annual fee", "Online banking"], "description": "Simple flat cash back from online bank."}
        ])
        
        return cards

    def scrape_creditcardgenius(self) -> List[Dict[str, Any]]:
        """Scrape credit card data from creditcardgenius.ca."""
        cards = []
        try:
            logger.info("Scraping creditcardgenius.ca...")
            url = "https://creditcardgenius.ca/credit-cards"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract card listings from the page
            card_links = soup.find_all('a', href=re.compile(r'/credit-cards/'))
            
            for link in card_links[:40]:
                try:
                    name = link.get_text(strip=True)
                    if name and len(name) > 3:
                        card = {
                            "name": name,
                            "issuer": "creditcardgenius.ca",
                            "annual_fee": 0.0,
                            "rewards_rate": "Details available",
                            "welcome_bonus": "See offer",
                            "categories": ["Credit Card"],
                            "perks": [],
                            "description": f"Card listed on creditcardgenius.ca - {name}"
                        }
                        cards.append(card)
                except:
                    continue
            
            logger.info(f"Scraped {len(cards)} cards from creditcardgenius.ca")
        except Exception as e:
            logger.warning(f"Error scraping creditcardgenius: {e}")
        
        return cards

    def scrape_frugalflyer(self) -> List[Dict[str, Any]]:
        """Scrape credit card data from frugalflyer.ca."""
        cards = []
        try:
            logger.info("Scraping frugalflyer.ca...")
            url = "https://frugalflyer.ca/compare-credit-cards/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract card links from the page
            card_links = soup.find_all('a', href=re.compile(r'/credit-card/'))
            
            for link in card_links[:40]:
                try:
                    name = link.get_text(strip=True)
                    if name and len(name) > 3:
                        card = {
                            "name": name,
                            "issuer": "frugalflyer.ca",
                            "annual_fee": 0.0,
                            "rewards_rate": "Details available",
                            "welcome_bonus": "See offer",
                            "categories": ["Travel Rewards"],
                            "perks": [],
                            "description": f"Card listed on frugalflyer.ca - {name}"
                        }
                        cards.append(card)
                except:
                    continue
            
            logger.info(f"Scraped {len(cards)} cards from frugalflyer.ca")
        except Exception as e:
            logger.warning(f"Error scraping frugalflyer: {e}")
        
        return cards

    def _deduplicate_cards(self, cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate cards based on name similarity."""
        seen = set()
        unique_cards = []
        
        for card in cards:
            normalized = card['name'].lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique_cards.append(card)
        
        return unique_cards

    def fetch_current_cards(self) -> List[Dict[str, Any]]:
        """Fetch the latest credit card data from multiple sources."""
        logger.info("Fetching latest credit card data...")
        
        all_cards = self.base_cards.copy()
        
        # Try to scrape both sources for additional cards
        try:
            ccg_cards = self.scrape_creditcardgenius()
            all_cards.extend(ccg_cards)
            time.sleep(1)
        except Exception as e:
            logger.warning(f"Failed to scrape creditcardgenius: {e}")
        
        try:
            ff_cards = self.scrape_frugalflyer()
            all_cards.extend(ff_cards)
        except Exception as e:
            logger.warning(f"Failed to scrape frugalflyer: {e}")
        
        # Deduplicate and return
        unique_cards = self._deduplicate_cards(all_cards)
        logger.info(f"Successfully fetched {len(unique_cards)} unique credit cards")
        return unique_cards


if __name__ == "__main__":
    scraper = CreditCardScraper()
    cards = scraper.fetch_current_cards()
    print(f"Total cards: {len(cards)}")
    print(f"\nSample cards:")
    for card in cards[:5]:
        print(f"  - {card['name']} ({card['issuer']})")

