"""This module contains the models and some tools for using them."""

from pathlib import Path
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


from pydantic import BaseModel


class Player(BaseModel):
    """A player is a participant in the secret santa draw."""

    name: str  # the player is identified with the name
    email: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Game(BaseModel):
    """A game game is a set of players."""

    name: str

    notification_template: str = "notification.html"
    notification_from: str = "Amigo Invisible <amigoinvisible@mgabarda.com>"
    notification_subject: str = "Sorteo Amigo Invisible"

    players: dict[str, Player]
    exclusions: list[tuple[str, str]]

    @classmethod
    def create(cls, config_file: Path) -> "Game":
        """Creates the game using the provided config file."""
        assert config_file.is_file(), f"The file {config_file} does not't exists."

        with config_file.open() as file:
            config = yaml.load(file, Loader=Loader)

        secret_santa_config = config["secret-santa"]

        # load players
        players = {
            participant["name"]: Player(
                name=participant["name"], email=participant["email"]
            )
            for participant in secret_santa_config["participants"]
        }

        # load exclusions
        exclusions = []
        for exclusion in secret_santa_config["exclusions"]:
            exclusions.append((exclusion["from"], exclusion["to"]))
            if exclusion.get("reverse", False):
                exclusions.append((exclusion["to"], exclusion["from"]))

        # create game
        game = cls(
            name=secret_santa_config["name"],
            players=players,
            exclusions=exclusions,
            template=secret_santa_config.get("template"),
        )

        # load notification if defined
        notification_config = secret_santa_config.get("notification")
        if notification_config.get("template"):
            game.notification_template = notification_config.get("template")
        if notification_config.get("subject"):
            game.notification_subject = notification_config.get("subject")

        return game

    def participants(self) -> list[str]:
        """Get the list of participants as used y the draw."""
        return [player.name for player in self.players.values()]
