"""
Game module for the Go Fish simulator.
Contains the core game logic and rules.
"""
import random
from typing import List, Optional, Dict, Tuple

from .cards import Card, Deck
from .player import Player


class GoFishGame:
    """
    Represents a game of Go Fish.
    This class encapsulates the rules and logic of the game.
    """
    
    def __init__(self, players: List[Player], initial_cards: int = 7, verbose: bool = True):
        """
        Initialize a new game of Go Fish.
        
        Args:
            players: List of Player objects
            initial_cards: Number of cards to deal to each player at the start
            verbose: Whether to print game progress messages
        """
        if len(players) < 2:
            raise ValueError("Go Fish requires at least 2 players")
        
        self.players = players
        self.initial_cards = initial_cards
        self.verbose = verbose
        self.deck = Deck()
        self.current_player_idx = 0
        self.game_over = False
        self.turn_count = 0
        
    def setup(self) -> None:
        """Set up the game by shuffling the deck and dealing cards."""
        self.deck.shuffle()
        
        # Deal initial cards to each player
        for player in self.players:
            cards = self.deck.draw_multiple(self.initial_cards)
            player.add_cards(cards)
            
            # Check for any books in the initial hand
            books = player.check_for_books()
            if books and self.verbose:
                print(f"{player.name} found {len(books)} book(s) in their initial hand: {', '.join(books)}")
    
    def play_turn(self) -> bool:
        """
        Play a single turn of the game.
        
        Returns:
            True if the game should continue, False if it's over
        """
        if self.game_over:
            return False
            
        self.turn_count += 1
        current_player = self.players[self.current_player_idx]
        
        if self.verbose:
            print(f"\n--- Turn {self.turn_count}: {current_player.name}'s turn ---")
        
        # Check if the current player has any cards
        if not current_player.has_cards():
            if self.deck.is_empty():
                if self.verbose:
                    print(f"{current_player.name} has no cards and the deck is empty.")
                self.advance_turn()
                return self.check_game_over()
            else:
                # Draw a card from the deck
                card = self.deck.draw()
                if card:
                    current_player.add_card(card)
                    if self.verbose:
                        print(f"{current_player.name} had no cards and drew {card} from the deck.")
                    
                    # Check for books
                    books = current_player.check_for_books()
                    if books and self.verbose:
                        print(f"{current_player.name} found a book of {books[0]}!")
        
        # Get other players' names
        other_players = [p.name for p in self.players if p != current_player]
        if not other_players:
            self.game_over = True
            return False
            
        # Choose a player to ask
        target_player_name = current_player.choose_player_to_ask(other_players)
        target_player = next(p for p in self.players if p.name == target_player_name)
        
        # Choose a rank to ask for
        rank = current_player.choose_rank_to_ask_for()
        if not rank:
            if self.verbose:
                print(f"{current_player.name} has no cards to ask for.")
            self.advance_turn()
            return self.check_game_over()
            
        if self.verbose:
            print(f"{current_player.name} asks {target_player_name} for {rank}s.")
        
        # Check if the target player has any cards of the requested rank
        matching_cards = [card for card in target_player.hand.cards if card.rank == rank]
        
        if matching_cards:
            # Target player has matching cards
            if self.verbose:
                print(f"{target_player_name} has {len(matching_cards)} {rank}(s)!")
                
            # Update knowledge
            current_player.update_knowledge(target_player_name, rank, True)
            
            # Transfer the cards
            for card in matching_cards:
                target_player.hand.remove_card(card)
                current_player.add_card(card)
                
            # Check for books
            books = current_player.check_for_books()
            if books and self.verbose:
                for book_rank in books:
                    print(f"{current_player.name} completed a book of {book_rank}s!")
                    
            # Player gets another turn
            return self.check_game_over()
        else:
            # Target player doesn't have matching cards
            if self.verbose:
                print(f"{target_player_name} says 'Go Fish!'")
                
            # Update knowledge
            current_player.update_knowledge(target_player_name, rank, False)
            
            # Draw a card from the deck
            if not self.deck.is_empty():
                card = self.deck.draw()
                if card:
                    current_player.add_card(card)
                    if self.verbose:
                        print(f"{current_player.name} draws a card from the deck.")
                        
                    # If the drawn card is the rank that was asked for, the player gets another turn
                    if card.rank == rank:
                        if self.verbose:
                            print(f"{current_player.name} drew the {card}, which is the rank they asked for!")
                            
                        # Check for books
                        books = current_player.check_for_books()
                        if books and self.verbose:
                            for book_rank in books:
                                print(f"{current_player.name} completed a book of {book_rank}s!")
                                
                        # Player gets another turn
                        return self.check_game_over()
            else:
                if self.verbose:
                    print("The deck is empty.")
            
            # Check for books
            books = current_player.check_for_books()
            if books and self.verbose:
                for book_rank in books:
                    print(f"{current_player.name} completed a book of {book_rank}s!")
            
            # Move to the next player
            self.advance_turn()
            return self.check_game_over()
    
    def advance_turn(self) -> None:
        """Advance to the next player's turn."""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
    
    def check_game_over(self) -> bool:
        """
        Check if the game is over.
        
        Returns:
            True if the game should continue, False if it's over
        """
        # Game is over if all players have no cards or if all cards have been formed into books
        all_cards_in_books = True
        for player in self.players:
            if player.has_cards():
                all_cards_in_books = False
                break
                
        if all_cards_in_books:
            self.game_over = True
            return False
            
        return True
    
    def get_winner(self) -> List[Player]:
        """
        Determine the winner(s) of the game.
        
        Returns:
            List of Player objects who have the highest score
        """
        if not self.game_over:
            return []
            
        max_score = max(player.get_score() for player in self.players)
        return [player for player in self.players if player.get_score() == max_score]
    
    def play_game(self) -> List[Player]:
        """
        Play a complete game of Go Fish.
        
        Returns:
            List of Player objects who won the game
        """
        self.setup()
        
        while self.play_turn():
            pass
            
        winners = self.get_winner()
        
        if self.verbose:
            print("\n--- Game Over ---")
            for player in self.players:
                print(f"{player.name}: {player.get_score()} books")
                
            if len(winners) == 1:
                print(f"\nThe winner is {winners[0].name} with {winners[0].get_score()} books!")
            else:
                winner_names = [player.name for player in winners]
                print(f"\nThe game ended in a tie between {', '.join(winner_names)} with {winners[0].get_score()} books each!")
        
        return winners