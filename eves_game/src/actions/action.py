from abc import ABC, abstractclassmethod


class Action(ABC):

    def __init__(self, player: 'Player', location: 'Location', locations: dict, item: 'Item', items: dict) -> None:
        self.player = player
        self.location = location
        self.locations = locations
        self.item = item
        self.items = items

    @abstractclassmethod
    def action(self) -> (bool, str):
        pass

    @property
    def action_group(self) -> str:
        return self._action_group

    @action_group.setter
    def action_group(self, value: str) -> None:
        if value in self.action_groups:
            self._action_group = value
        else:
            raise ValueError(f"This isn't a support action group {value}.")

    @property
    def action_groups(cls) -> list[str]:
        return ['Player', 'Location', 'MoveLocation']

    def return_game_state(self) -> ('player', 'location', 'locations', 'item', 'items'):
        return self.player, self.location, self.locations, self.item, self.items
