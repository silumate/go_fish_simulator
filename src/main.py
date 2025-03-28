#!/usr/bin/env python3
"""
Go Fish Simulator - Main Entry Point

This script provides a command-line interface to run Go Fish simulations
with various player types and configurations.
"""
import argparse
import random
import sys
from typing import List, Optional

from gofish.cards import Card, Deck
from gofish.player import Player, RandomPlayer, SmartPlayer, MemoryPlayer, HumanPlayer
from gofish.game import GoFishGame


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Go Fish Simulator')
    
    parser.add_argument(
        '--players', 
        type=int, 
        default=4,
        help='Number of players (default: 4)'
    )
    
    parser.add_argument(
        '--human', 
        action='store_true',
        help='Include a human player'
    )
    
    parser.add_argument(
        '--initial-cards', 
        type=int, 
        default=7,
        help='Number of cards to deal to each player initially (default: 7)'
    )
    
    parser.add_argument(
        '--quiet', 
        action='store_true',
        help='Run in quiet mode (no verbose output)'
    )
    
    parser.add_argument(
        '--games', 
        type=int, 
        default=1,
        help='Number of games to simulate (default: 1)'
    )
    
    parser.add_argument(
        '--player-types',
        type=str,
        default='random',
        help='Comma-separated list of player types: random, smart, memory (default: random)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducible results'
    )
    
    return parser.parse_args()


def create_players(args) -> List[Player]:
    """
    Create players based on command-line arguments.
    
    Args:
        args: Command-line arguments
        
    Returns:
        List of Player objects
    """
    players = []
    player_types = args.player_types.split(',')
    
    # Validate player types
    valid_types = {'random', 'smart', 'memory'}
    for pt in player_types:
        if pt not in valid_types:
            print(f"Error: Invalid player type '{pt}'. Valid types are: {', '.join(valid_types)}")
            sys.exit(1)
    
    # Create human player if requested
    if args.human:
        players.append(HumanPlayer("Human"))
    
    # Create AI players
    num_ai_players = args.players - (1 if args.human else 0)
    for i in range(num_ai_players):
        player_type = player_types[i % len(player_types)]
        
        if player_type == 'random':
            players.append(RandomPlayer(f"Random-{i+1}"))
        elif player_type == 'smart':
            players.append(SmartPlayer(f"Smart-{i+1}"))
        elif player_type == 'memory':
            players.append(MemoryPlayer(f"Memory-{i+1}"))
    
    return players


def run_simulation(args):
    """
    Run a Go Fish simulation with the specified parameters.
    
    Args:
        args: Command-line arguments
    """
    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
    
    # Track statistics across multiple games
    win_counts = {}
    
    for game_num in range(args.games):
        if args.games > 1 and not args.quiet:
            print(f"\n=== Game {game_num + 1} of {args.games} ===\n")
        
        # Create players for this game
        players = create_players(args)
        
        # Initialize and run the game
        game = GoFishGame(
            players=players,
            initial_cards=args.initial_cards,
            verbose=not args.quiet
        )
        
        winners = game.play_game()
        
        # Update win statistics
        for winner in winners:
            win_counts[winner.name] = win_counts.get(winner.name, 0) + 1
    
    # Print overall statistics for multiple games
    if args.games > 1:
        print("\n=== Final Statistics ===")
        print(f"Total games: {args.games}")
        print("\nWin counts:")
        
        # Sort by win count (descending)
        sorted_wins = sorted(win_counts.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_wins:
            win_percentage = (count / args.games) * 100
            print(f"{name}: {count} wins ({win_percentage:.1f}%)")


def main():
    """Main entry point for the Go Fish simulator."""
    args = parse_args()
    run_simulation(args)


if __name__ == "__main__":
    main()