from dataclasses import dataclass, field
import uuid


@dataclass
class ActionReference():
    """
    Represents a reference to an action in the game.

    Attributes:
        id (str): The unique identifier of the action type as a string.
        name (str): The name of the action.
        description (str): The description of the action.
        action_type (str): The type of the action i.e. location, player, move.
        actionID (str): The unique identifier of the action as a string.
    """
    id: str
    name: str
    description: str
    action_type: str
    actionID: str = field(default=str(uuid.uuid4()))


class ActionListManager():

    def __init__(self, location: 'Location', player: 'Player', items: dict['Item'], locations: dict['Location'], logger: 'Logger') -> None:
        """
        Initializes an instance of the ActionListManager class.

        Args:
            location (Location): The current location in the game.
            player (Player): The player object.
            items (dict['Item']): A dictionary of items in the game.
            locations (dict['Location']): A dictionary of locations in the game.
            logger (Logger): The logger object for logging game events.
        """
        self.location = location
        self.player = player
        self.items = items
        self.locations = locations
        self.logger = logger
        self.action_list = [ActionReference]

    def get_action_type(action_description: str) -> str:
        pass

    def _location_items_actions(self) -> None:
        """
        Retrieves the actions associated with the location items and adds them to the action list.

        Returns:
            None
        """
        for self.item, (self.value) in enumerate(self.location.location_items):
            self.actions = self.items[str(self.value)].actions.items()
            self.logger.debug(f'Location actions for Action List for {self.items[str(self.value)].item_description}: '
                              f'{self.actions} total actions: {len(self.actions)}')

            for self.action in self.actions:
                self.action_name, self.action_details = self.action
                if self.action_details['holding'] == 'No':
                    self.newActionReference = ActionReference(
                        self.action_details['action_id'], self.action_name, self.action_details['action_description'], 'location')
                    self.action_list.append(self.newActionReference)

                self.logger.debug(f'Location actions {self.action_details['action_id']}, '
                                  f'{self.action_name}, {self.action_details['action_description']}, location')

    def _location_move_actions(self) -> None:
        """
        Generates move actions for the Action List based on the possible moves of the current location.
        Each move action is added to the action list.
        """
        for self.key, self.value in enumerate(self.location.location_possible_moves):
            self.newActionReference = ActionReference(
                self.value, self.value, self.value, 'move_location')
            self.action_list.append(self.newActionReference)

    def create_action_list(self) -> list[dict]:
        pass
