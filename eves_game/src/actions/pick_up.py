from src.actions.action import Action


class PickUp(Action):

    def __init__(self, player: 'Player', location: 'Location', item: 'item', **kwargs) -> None:
        self.player = player
        self.location = location
        self.item = item
        super().__init__()

    def action(self) -> (bool, str):

        if (self.player.player_items_length < self.player.max_item_length):
            try:
                if self.player.add_item(self.item):
                    self.success = True
                    self.player_msg = f'You have picked up {
                        self.item.item_name}'
                    self.location.location_items.remove(self.item.item_id)
                    return (self.success, self.player_msg)
            except:
                self.success = False
                self.player_msg = f'Sorry, unable to pick up {
                    self.item.item_name}'
                return (self.success, self.player_msg)
        else:
            self.success = False
            self.player_msg = 'Sorry, you are already holding the maximum number of items'
            return (self.success, self.player_msg)