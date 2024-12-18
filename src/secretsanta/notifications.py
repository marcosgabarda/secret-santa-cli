"""This module handles the notification process of the result of a draw."""

import logging
from pathlib import Path

import httpx
from jinja2 import Environment, FileSystemLoader, Template

from . import settings
from .draws import Draw
from .models import Game, Player

logger = logging.getLogger(__name__)


def single_notification(
    game: Game,
    template: Template,
    players: tuple[Player, Player],
    dry: bool = False,
) -> None:
    """Sends a single notification."""

    # from player 0 to player 1
    _from = players[0]
    _to = players[1]

    content = template.render(
        from_name=_from.name,
        to_name=_to.name,
    )

    if dry:
        print("From:", game.notification_from)
        print("To:", _from.email)
        print("Subject:", game.notification_subject)
        print("---")
        print(content)
        print("---\n")
    else:
        response = httpx.post(
            f"{settings.mailgun_api_url}/messages",
            auth=("api", settings.mailgun_api_key.get_secret_value()),
            data={
                "from": game.notification_from,
                "to": [_from.email],
                "subject": game.notification_subject,
                "html": content,
            },
        )
        response.raise_for_status()


def notify(game: Game, draw: Draw, dry: bool = False) -> None:
    """Notify the result of the draw in the game."""

    # load template
    if game.notification_template:
        environment = Environment()
        template = environment.from_string(game.notification_template)
    else:
        templates_path = Path(__file__).parent / "templates"
        environment = Environment(loader=FileSystemLoader(templates_path))
        template = environment.get_template(game.notification_template_file)

    # iterate over solution
    for _from_name, _to_name in draw.solution:
        players = (game.players[_from_name], game.players[_to_name])
        single_notification(game=game, template=template, players=players, dry=dry)
