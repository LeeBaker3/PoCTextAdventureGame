from src.actions.action import Action


class MoveLocation(Action):

    def __init__(self, selected_action: str, player: 'Player', location: 'Location', locations: dict, item: 'Item', items: dict, logger: 'Logger') -> None:
        self.selected_action = selected_action
        # self.player = player
        # self.location = location
        # self.locations = locations
        # self.item = item
        # self.items = items
        self.action_group = 'MoveLocation'
        self.logger = logger
        super().__init__(player, location, locations, item, items)

    def _search_possible_moves(self) -> str:
        self.possible_moves = self.location.location_possible_moves
        result = [key for key, value in self.possible_moves.items() if value.description ==
                  self.selected_action]
        self.logger.debug(f'possible_moves: {self.possible_moves.items()}')
        self.logger.debug(f'result: {result}')
        if result:
            return result[0]
        return None

    def action(self) -> (bool, str):

        new_location_key = self._search_possible_moves()

        if new_location_key != None:
            self.logger.debug(f"key Value for new location: {
                              new_location_key}")
            self.location = self.locations[new_location_key[0]]
            self.success = True
            self.player_msg = (f"You have moved to {
                               self.location.location_description}")
            return (self.success, self.player_msg)
        else:
            self.success = False
            self.player_msg = (
                f"That doesn't match any of the possible actions")
            return (self.success, self.player_msg)
