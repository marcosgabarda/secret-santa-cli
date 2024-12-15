"""Main module."""

import argparse
from pathlib import Path
import sys

from santa.draws import Draw
from santa.models import Game
from santa.notifications import notify


def main() -> None:
    """Main function."""

    # loads game config
    parser = argparse.ArgumentParser(description="Secret Santa CLI tool.")
    parser.add_argument(
        "config",
        type=str,
        help="Path to .yaml file with the configuration of the Secret Santa game.",
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
    notify(game=game, draw=draw)


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
