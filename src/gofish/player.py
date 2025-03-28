"""
Player module for the Go Fish simulator.
Defines the Player interface and various player strategy implementations.
"""
import random
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Set, Tuple

from .cards import Card, Hand


class Player(ABC):
    """Abstract base class for a Go Fish player."""
    
    def __init__(self, name: str):
        """
        Initialize a player.
        
        Args:
            name: The player's name
        """
        self.name = name
        self.hand = Hand()
        self.books = []  # List of ranks for which the player has collected books
        self.known_cards: Dict[str, Set[str]] = {}  # Player's knowledge of other players' cards
    
    def __str__(self) -> str:
        """Return a string representation of the player."""
        return f"{self.name} (Books: {len(self.books)})"
    
    def add_card(self, card: Card) -> None:
        """
        Add a card to the player's hand.
        
        Args:
            card: The Card object to add
        """
        self.hand.add_card(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """
        Add multiple cards to the player's hand.
        
        Args:
            cards: List of Card objects to add
        """
        self.hand.add_cards(cards)
    
    def check_for_books(self) -> List[str]:
        """
        Check for and remove any books from the player's hand.
        
        Returns:
            List of ranks for which books were found and removed
        """
        new_books = self.hand.find_books()
        for book_rank in new_books:
            self.books.append(book_rank)
            self.hand.remove_cards_of_rank(book_rank)
        return new_books
    
    def has_cards(self) -> bool:
        """Check if the player has any cards in their hand."""
        return len(self.hand) > 0
    
    def get_score(self) -> int:
        """Get the player's score (number of books)."""
        return len(self.books)
    
    def update_knowledge(self, player_name: str, rank: str, has_card: bool) -> None:
        """
        Update the player's knowledge about other players' cards.
        
        Args:
            player_name: The name of the player to update knowledge about
            rank: The rank that was asked for
            has_card: Whether the player has the card or not
        """
        if player_name not in self.known_cards:
            self.known_cards[player_name] = set()
            
        if has_card:
            self.known_cards[player_name].add(rank)
        elif rank in self.known_cards[player_name]:
            self.known_cards[player_name].remove(rank)
    
    @abstractmethod
    def choose_rank_to_ask_for(self) -> Optional[str]:
        """
        Choose a rank to ask another player for.
        
        Returns:
            The rank to ask for, or None if the player has no cards
        """
        pass
    
    @abstractmethod
    def choose_player_to_ask(self, player_names: List[str]) -> str:
        """
        Choose a player to ask for a card.
        
        Args:
            player_names: List of other players' names
            
        Returns:
            The name of the player to ask
        """
        pass


class RandomPlayer(Player):
    """A player that makes random choices."""
    
    def choose_rank_to_ask_for(self) -> Optional[str]:
        """
        Choose a random rank from the player's hand.
        
        Returns:
            A random rank from the player's hand, or None if the hand is empty
        """
        ranks = self.hand.get_ranks()
        if not ranks:
            return None
        return random.choice(ranks)
    
    def choose_player_to_ask(self, player_names: List[str]) -> str:
        """
        Choose a random player to ask.
        
        Args:
            player_names: List of other players' names
            
        Returns:
            A random player name from the list
        """
        return random.choice(player_names)


class SmartPlayer(Player):
    """A player that makes strategic choices based on known information."""
    
    def choose_rank_to_ask_for(self) -> Optional[str]:
        """
        Choose a rank to ask for based on the player's hand and knowledge.
        Prioritizes ranks that the player already has multiple cards of.
        
        Returns:
            The chosen rank, or None if the hand is empty
        """
        if not self.has_cards():
            return None
            
        # Count the occurrences of each rank in the hand
        rank_counts = {}
        for card in self.hand.cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        
        # Sort ranks by count (descending) to prioritize ranks with more cards
        sorted_ranks = sorted(rank_counts.keys(), key=lambda r: rank_counts[r], reverse=True)
        return sorted_ranks[0]
    
    def choose_player_to_ask(self, player_names: List[str]) -> str:
        """
        Choose a player to ask based on known information.
        Prioritizes players known to have the rank we're looking for.
        
        Args:
            player_names: List of other players' names
            
        Returns:
            The chosen player name
        """
        rank_to_ask = self.choose_rank_to_ask_for()
        
        # Check if we know any player has the rank we're looking for
        for player_name in player_names:
            if player_name in self.known_cards and rank_to_ask in self.known_cards[player_name]:
                return player_name
        
        # Otherwise, choose a random player
        return random.choice(player_names)


class MemoryPlayer(Player):
    """A player that remembers which cards other players have asked for."""
    
    def __init__(self, name: str):
        """
        Initialize a memory player.
        
        Args:
            name: The player's name
        """
        super().__init__(name)
        self.asked_ranks: Dict[str, Set[str]] = {}  # Ranks that other players have asked for
    
    def record_ask(self, player_name: str, rank: str) -> None:
        """
        Record that a player has asked for a specific rank.
        
        Args:
            player_name: The name of the player who asked
            rank: The rank they asked for
        """
        if player_name not in self.asked_ranks:
            self.asked_ranks[player_name] = set()
        self.asked_ranks[player_name].add(rank)
    
    def choose_rank_to_ask_for(self) -> Optional[str]:
        """
        Choose a rank to ask for based on the player's hand and memory.
        
        Returns:
            The chosen rank, or None if the hand is empty
        """
        if not self.has_cards():
            return None
            
        # Count the occurrences of each rank in the hand
        rank_counts = {}
        for card in self.hand.cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        
        # Sort ranks by count (descending) to prioritize ranks with more cards
        sorted_ranks = sorted(rank_counts.keys(), key=lambda r: rank_counts[r], reverse=True)
        return sorted_ranks[0]
    
    def choose_player_to_ask(self, player_names: List[str]) -> str:
        """
        Choose a player to ask based on memory of what they've asked for.
        
        Args:
            player_names: List of other players' names
            
        Returns:
            The chosen player name
        """
        rank_to_ask = self.choose_rank_to_ask_for()
        
        # Check if any player has asked for the rank we're looking for
        for player_name in player_names:
            if (player_name in self.asked_ranks and 
                rank_to_ask in self.asked_ranks[player_name]):
                return player_name
        
        # Otherwise, choose a random player
        return random.choice(player_names)


class HumanPlayer(Player):
    """A player controlled by a human user."""
    
    def choose_rank_to_ask_for(self) -> Optional[str]:
        """
        Ask the human user which rank to ask for.
        
        Returns:
            The chosen rank, or None if the hand is empty
        """
        if not self.has_cards():
            return None
            
        # Display the player's hand
        print(f"\nYour hand:")
        ranks = {}
        for card in self.hand.cards:
            if card.rank not in ranks:
                ranks[card.rank] = []
            ranks[card.rank].append(card)
        
        for rank, cards in ranks.items():
            print(f"{rank}: {', '.join(str(card) for card in cards)}")
        
        # Ask the user which rank to ask for
        while True:
            rank = input("\nWhich rank would you like to ask for? ").strip().upper()
            if rank == '10':
                pass  # 10 is a valid rank
            elif len(rank) == 1:
                rank = rank.upper()  # Convert single character to uppercase
            
            if rank in self.hand.get_ranks():
                return rank
            else:
                print("You must ask for a rank that you have in your hand.")
    
    def choose_player_to_ask(self, player_names: List[str]) -> str:
        """
        Ask the human user which player to ask.
        
        Args:
            player_names: List of other players' names
            
        Returns:
            The chosen player name
        """
        print("\nOther players:")
        for i, name in enumerate(player_names, 1):
            print(f"{i}. {name}")
        
        while True:
            try:
                choice = int(input("\nWhich player would you like to ask? (enter number) "))
                if 1 <= choice <= len(player_names):
                    return player_names[choice - 1]
                else:
                    print(f"Please enter a number between 1 and {len(player_names)}.")
            except ValueError:
                print("Please enter a valid number.")