"""
Card library for the Go Fish simulator.
Provides classes and methods to manipulate cards and decks.
"""
import random
from typing import List, Optional, Tuple


class Card:
    """Represents a standard playing card."""
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    
    def __init__(self, rank: str, suit: str):
        """
        Initialize a card with a rank and suit.
        
        Args:
            rank: The rank of the card (2-10, J, Q, K, A)
            suit: The suit of the card (Hearts, Diamonds, Clubs, Spades)
        """
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
            
        self.rank = rank
        self.suit = suit
    
    def __str__(self) -> str:
        """Return a string representation of the card."""
        return f"{self.rank} of {self.suit}"
    
    def __eq__(self, other) -> bool:
        """Check if two cards are equal (same rank and suit)."""
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def same_rank(self, other) -> bool:
        """Check if two cards have the same rank."""
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank


class Deck:
    """Represents a deck of playing cards."""
    
    def __init__(self, cards: Optional[List[Card]] = None):
        """
        Initialize a deck of cards.
        
        Args:
            cards: Optional list of cards to initialize the deck with.
                  If None, a standard 52-card deck is created.
        """
        if cards is not None:
            self.cards = cards.copy()
        else:
            self.cards = [Card(rank, suit) 
                         for suit in Card.SUITS 
                         for rank in Card.RANKS]
    
    def __len__(self) -> int:
        """Return the number of cards in the deck."""
        return len(self.cards)
    
    def shuffle(self) -> None:
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)
    
    def draw(self) -> Optional[Card]:
        """
        Draw a card from the top of the deck.
        
        Returns:
            A Card object if the deck is not empty, None otherwise.
        """
        if not self.cards:
            return None
        return self.cards.pop(0)
    
    def draw_multiple(self, count: int) -> List[Card]:
        """
        Draw multiple cards from the top of the deck.
        
        Args:
            count: Number of cards to draw
            
        Returns:
            A list of Card objects (may be fewer than requested if deck runs out)
        """
        drawn_cards = []
        for _ in range(min(count, len(self.cards))):
            card = self.draw()
            if card:
                drawn_cards.append(card)
        return drawn_cards
    
    def add_card(self, card: Card) -> None:
        """
        Add a card to the bottom of the deck.
        
        Args:
            card: The Card object to add
        """
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """
        Add multiple cards to the bottom of the deck.
        
        Args:
            cards: List of Card objects to add
        """
        self.cards.extend(cards)
    
    def is_empty(self) -> bool:
        """Check if the deck is empty."""
        return len(self.cards) == 0


class Hand:
    """Represents a player's hand of cards."""
    
    def __init__(self):
        """Initialize an empty hand."""
        self.cards = []
    
    def __len__(self) -> int:
        """Return the number of cards in the hand."""
        return len(self.cards)
    
    def add_card(self, card: Card) -> None:
        """
        Add a card to the hand.
        
        Args:
            card: The Card object to add
        """
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """
        Add multiple cards to the hand.
        
        Args:
            cards: List of Card objects to add
        """
        self.cards.extend(cards)
    
    def remove_card(self, card: Card) -> bool:
        """
        Remove a specific card from the hand.
        
        Args:
            card: The Card object to remove
            
        Returns:
            True if the card was removed, False if it wasn't in the hand
        """
        for i, c in enumerate(self.cards):
            if c == card:
                self.cards.pop(i)
                return True
        return False
    
    def remove_cards_of_rank(self, rank: str) -> List[Card]:
        """
        Remove all cards of a specific rank from the hand.
        
        Args:
            rank: The rank to remove
            
        Returns:
            List of Card objects that were removed
        """
        removed_cards = []
        self.cards, removed_cards = self._partition_cards(lambda c: c.rank != rank)
        return removed_cards
    
    def _partition_cards(self, predicate) -> Tuple[List[Card], List[Card]]:
        """
        Helper method to partition cards based on a predicate.
        
        Args:
            predicate: Function that takes a Card and returns a boolean
            
        Returns:
            Tuple of (cards_that_match, cards_that_dont_match)
        """
        matching = []
        non_matching = []
        
        for card in self.cards:
            if predicate(card):
                matching.append(card)
            else:
                non_matching.append(card)
                
        return matching, non_matching
    
    def has_rank(self, rank: str) -> bool:
        """
        Check if the hand contains a card of the specified rank.
        
        Args:
            rank: The rank to check for
            
        Returns:
            True if the hand contains at least one card of the specified rank
        """
        return any(card.rank == rank for card in self.cards)
    
    def get_ranks(self) -> List[str]:
        """
        Get a list of all ranks in the hand.
        
        Returns:
            List of rank strings
        """
        return list(set(card.rank for card in self.cards))
    
    def find_books(self) -> List[str]:
        """
        Find all books (sets of 4 cards of the same rank) in the hand.
        
        Returns:
            List of ranks that form books
        """
        rank_counts = {}
        for card in self.cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        
        return [rank for rank, count in rank_counts.items() if count == 4]
    
    def remove_books(self) -> List[List[Card]]:
        """
        Remove all books from the hand.
        
        Returns:
            List of books (each book is a list of 4 Card objects)
        """
        books = []
        for rank in self.find_books():
            cards = [card for card in self.cards if card.rank == rank]
            books.append(cards)
            self.cards = [card for card in self.cards if card.rank != rank]
        
        return books