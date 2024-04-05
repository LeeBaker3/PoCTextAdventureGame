from inspect import getmembers, isclass, isabstract
from logging import Logger
import src.actions as actions
from src.items.item import Item
from src.locations.location import Location
from src.player.player import Player


class ActionFactory(object):
    action_implementations = {}

    def __init__(self) -> None:
        """
        Initializes the ActionFactory object.
        """
        self.load_actions_types()

    def load_actions_types(self) -> None:
        """
        Load the available action types into the action factory.

        This method retrieves all the implementations of the `Action` class from the `actions` module
        and stores them in the `action_implementations` dictionary, using the class name as the key.

        Note:
        - Only concrete classes that inherit from the `Action` class are considered.
        - Abstract classes are excluded from the list of implementations.

        Returns:
        None
        """
        implementations = getmembers(
            actions, lambda a: isclass(a) and not isabstract(a))
        for name, _type in implementations:
            if isclass(_type) and issubclass(_type, actions.Action):
                self.action_implementations[name] = _type

    def create(self, action_name: str, player: 'Player', location: 'Location', locations: dict, item: 'Item', items: dict, logger: 'Logger', selected_action: str) -> object:
        if action_name in self.action_implementations:
            return self.action_implementations[action_name](selected_action, player, location, locations, item, items, logger)
        else:
            raise ValueError(f'{action_name} is not currently implemented')
