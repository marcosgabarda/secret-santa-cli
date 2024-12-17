"""This module contains the logic of the draw."""

import logging
import random

from . import settings

logger = logging.getLogger(__name__)


class Draw:
    """This class represents the secret santa draw, handling the participants as a list
    of strings.
    """

    # list of all the participants
    participants: list[str]

    # current solution status, a list of pairs of participants
    solution: list[tuple[str, str]]

    # available participants
    available: set[str]

    # list of pair of participants that can't be assigned
    exclusions: list[tuple[str, str]]

    def __init__(
        self,
        participants: list[str],
        exclusions: list[tuple[str, str]] | None = None,
    ):
        """Initializes the draw."""
        self.participants = participants
        self.solution = []
        self.available = set(participants)
        self.exclusions = exclusions or []

    def __len__(self) -> int:
        """The len of the draw is the len of the current solution."""
        return len(self.solution)

    def is_complete(self) -> bool:
        """Draw is complete when the solution covers all the nodes, except for the
        transition that completes the cycle.
        """
        return len(self.solution) == len(self.participants) - 1

    def is_valid(self, transition: tuple[str, str]) -> bool:
        """A transition is valid if it is not in the exclusion list and not in the
        current solution.
        """
        return transition not in self.exclusions and transition not in self.solution

    def closing_transition(self) -> tuple[str, str]:
        """Creates the closing transition."""
        return (self.solution[-1][1], self.solution[0][0])

    def pick(self) -> str:
        """Selects the next possible participant."""
        if not self.solution:
            selected = random.choice(list(self.available))
            self.available.remove(selected)
        else:
            selected = self.solution[-1][1]  # select the last node in the solution
        return selected

    def add(self, candidate: tuple[str, str]) -> None:
        """Adds the candidate to the solution."""
        self.solution.append(candidate)
        if self.available:
            self.available.remove(candidate[1])

    def rollback(self, candidate: tuple[str, str]) -> None:
        """Undoes the candidate."""
        self.solution.remove(candidate)
        if self.available:
            self.available.add(candidate[1])

    def choices(self) -> list[str]:
        """Shuffle list of choices."""
        choices = list(self.available)
        random.shuffle(choices)
        return choices

    def backtrack(self) -> bool:
        """Executes a backtrack algorithm to find a solution to the draw (a solution)."""
        if self.is_complete():
            candidate = self.closing_transition()
            if self.is_valid(candidate):
                self.add(candidate)
                logger.info("Solution complete!")
                return True

        logger.debug("Partial solution...")

        current = self.pick()
        logger.debug("Let's pick %s and remove it from available", current)

        for selected in self.choices():
            logger.debug("Selected %s as possible candidate", selected)

            # build transition candidate
            candidate = (current, selected)

            # if the candidate is valid
            if self.is_valid(candidate):
                # build the partial solution
                self.add(candidate)
                # check the partial solution
                logger.debug("- Path: %s", str(self.solution))
                logger.debug("- Available: %s", str(self.available))
                if self.backtrack():
                    logger.debug("Candidate %s consolidated!", str(candidate))
                    return True
                # if this partial solution can't be finished, rollback
                self.rollback(candidate)
                logger.debug("Candidate %s rollback", str(candidate))

        return False

    def reset(self) -> None:
        """Restores the draw to the initial status."""
        self.solution = []
        self.available = set(self.participants)

    def run(self) -> None:
        """Executes the backtrack algorithm until gets a result."""
        for _ in range(settings.limit):
            if self.backtrack():
                break
            self.reset()
