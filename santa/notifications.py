"""This module handles the notification process of the result of a draw."""

import logging

import httpx
from jinja2 import Environment, FileSystemLoader, Template

from . import settings
from .models import Player, Game
from .draws import Draw

logger = logging.getLogger(__name__)


def single_notification(
    game: Game, template: Template, players: tuple[Player, Player]
) -> None:
    """Sends a single notification."""

    # from player 0 to player 1
    _from = players[0]
    _to = players[1]

    content = template.render(
        from_name=_from.name,
        to_name=_to.name,
    )

    # set to email
    destinies = []
    if settings.debug and settings.debug_to_email:
        destinies = [settings.debug_to_email]
    else:
        destinies = [_from.email]

    if destinies:
        response = httpx.post(
            f"{settings.mailgun_api_url}/messages",
            auth=("api", settings.mailgun_api_key.get_secret_value()),
            data={
                "from": game.notification_from,
                "to": destinies,
                "subject": game.notification_subject,
                "html": content,
            },
        )
        response.raise_for_status()


def notify(game: Game, draw: Draw) -> None:
    """Notify the result of the draw in the game."""

    # load template
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template(game.notification_template)

    # iterate over solution
    for _from_name, _to_name in draw.solution:
        players = (game.players[_from_name], game.players[_to_name])
        single_notification(game=game, template=template, players=players)
