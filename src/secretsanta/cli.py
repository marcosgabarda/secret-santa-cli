"""Main module."""

import argparse
import sys
from pathlib import Path

from .draws import Draw
from .models import Game
from .notifications import notify


def app() -> None:
    """Main app function, entry point for the CLI, using argparse."""
    # loads game config
    parser = argparse.ArgumentParser(description="Secret Santa CLI tool.")
    parser.add_argument(
        "config",
        type=str,
        help="Path to .yaml file with the configuration of the Secret Santa game.",
    )
    parser.add_argument(
        "--dry",
        action="store_true",
        help="Simulates the game, and doesn't sends the result.",
    )
    args = parser.parse_args()
    config_file = Path(args.config)
    if not config_file.is_file():
        print("Game config file not found!")
        sys.exit(1)
    # creates the game
    game = Game.create(config_file=config_file)
    # runs the draw
    draw = Draw(participants=game.participants(), exclusions=game.exclusions)
    draw.run()
    # notify the results
    notify(game=game, draw=draw, dry=args.dry)


if __name__ == "__main__":
    app()
