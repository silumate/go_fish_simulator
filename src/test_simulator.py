#!/usr/bin/env python3
"""
Test script for the Go Fish simulator.
This script runs a simple game with predefined players to verify functionality.
"""
import random
from gofish.cards import Card, Deck
from gofish.player import RandomPlayer, SmartPlayer, MemoryPlayer
from gofish.game import GoFishGame


def test_basic_game():
    """Run a basic game with 4 players of different types."""
    print("=== Testing Basic Game ===")
    
    # Set a fixed seed for reproducibility
    random.seed(42)
    
    # Create players
    players = [
        RandomPlayer("Random-1"),
        SmartPlayer("Smart-1"),
        MemoryPlayer("Memory-1"),
        RandomPlayer("Random-2")
    ]
    
    # Create and run the game
    game = GoFishGame(players=players, initial_cards=5, verbose=True)
    winners = game.play_game()
    
    # Print results
    print("\nTest completed successfully!")
    print(f"Winner(s): {', '.join(player.name for player in winners)}")
    
    return True


def test_card_functionality():
    """Test basic card and deck functionality."""
    print("\n=== Testing Card Functionality ===")
    
    # Create a deck
    deck = Deck()
    print(f"Created a new deck with {len(deck)} cards")
    
    # Shuffle the deck
    deck.shuffle()
    print("Shuffled the deck")
    
    # Draw some cards
    cards = deck.draw_multiple(5)
    print(f"Drew 5 cards: {', '.join(str(card) for card in cards)}")
    print(f"Remaining cards in deck: {len(deck)}")
    
    # Test card equality
    card1 = Card("A", "Spades")
    card2 = Card("A", "Spades")
    card3 = Card("A", "Hearts")
    
    print(f"card1 == card2: {card1 == card2}")  # Should be True
    print(f"card1 == card3: {card1 == card3}")  # Should be False
    print(f"card1.same_rank(card3): {card1.same_rank(card3)}")  # Should be True
    
    return True


def test_player_strategies():
    """Test different player strategies."""
    print("\n=== Testing Player Strategies ===")
    
    # Create a deck and draw some cards
    deck = Deck()
    deck.shuffle()
    
    # Create players
    random_player = RandomPlayer("Random")
    smart_player = SmartPlayer("Smart")
    memory_player = MemoryPlayer("Memory")
    
    # Deal cards to players
    for player in [random_player, smart_player, memory_player]:
        cards = deck.draw_multiple(5)
        player.add_cards(cards)
        print(f"{player.name}'s hand: {', '.join(str(card) for card in player.hand.cards)}")
    
    # Test strategy choices
    other_players = ["Player1", "Player2", "Player3"]
    
    for player in [random_player, smart_player, memory_player]:
        rank = player.choose_rank_to_ask_for()
        target = player.choose_player_to_ask(other_players)
        print(f"{player.name} chooses to ask {target} for {rank}s")
    
    return True


def main():
    """Run all tests."""
    tests = [
        test_card_functionality,
        test_player_strategies,
        test_basic_game
    ]
    
    all_passed = True
    for test in tests:
        try:
            result = test()
            all_passed = all_passed and result
        except Exception as e:
            print(f"Test failed with error: {e}")
            all_passed = False
    
    if all_passed:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")


if __name__ == "__main__":
    main()