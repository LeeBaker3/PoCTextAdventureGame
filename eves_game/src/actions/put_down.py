from logging import Logger
from src.actions.action import Action
from src.items.item import Item
from src.locations.location import Location
from src.player.player import Player


class PutDown(Action):

    def __init__(self, selected_action: 'str', player: 'Player', location: 'Location', locations: dict, item: 'Item', items: dict, logger: 'Logger') -> None:
        self.selected_action = selected_action
        self.logger = logger
        self.action_group = 'Player'
        super().__init__(player, location, locations, item, items)

    def action(self) -> (bool, str):
        if self.player.remove_item(self.item):
            self.success = True
            self.player_msg = f'You have put down {self.item.item_name}'
            self.location.location_items.append(self.item.item_id)
            return (self.success, self.player_msg)
        else:
            self.success = False
            self.player_msg = f'Sorry, unable to put down {
                self.item.item_name}'
            return (self.success, self.player_msg)
