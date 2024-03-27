from dataclasses import dataclass, field
import uuid


@dataclass
class ActionReference:
    """
    Represents a reference to an action in the game.

    Attributes:
        id (str): The unique identifier of the action type as a string.
        name (str): The name of the action.
        description (str): The description of the action.
        action_type (str): The type of the action i.e. location, player, move.
        actionID (str): The unique identifier of the action as a string.
    """
    id: str = field(repr=True)
    name: str = field(repr=True)
    description: str = field(repr=True)
    action_type: str = field(repr=True)
    actionID: str = field(default=str(uuid.uuid4()))

    def __str__(self) -> str:
        return f'ActionReference: {self.id}, {self.name}, {self.description}, {self.action_type}'


class ActionListManager:

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
        self.action_reference_list = []

    def get_action_type_for_action_description(self, action_description: str) -> str:
        """
        Retrieves the action type based on the given action description.

        Args:
            action_description (str): The description of the action.

        Returns:
            str: The action type associated with the given action description.
                 Returns an empty string if no matching action is found.
        """
        for action_ref in self.action_reference_list:
            if action_ref.description == action_description:
                return action_ref.action_type
        return None

    def _location_actions(self) -> None:
        """
        Retrieves the actions associated with the location items and adds them to the action list.

        Returns:
            None
        """
        for self.item, (self.value) in enumerate(self.location.location_items):
            self.actions = self.items[self.value].actions.items()
            self.logger.debug(f'Location actions for Action List for {self.items[str(self.value)].item_description}: '
                              f'{self.actions} total actions: {len(self.actions)}')

            for self.action_ref in self.actions:
                self.action_name, self.action_details = self.action_ref
                if self.action_details['holding'] == 'No':
                    self.newActionReference = ActionReference(
                        self.action_details['action_id'], self.action_name, self.action_details['action_description'], 'Location')
                    self.action_reference_list.append(self.newActionReference)

                self.logger.debug(f'Location actions {self.action_details['action_id']}, '
                                  f'{self.action_name}, {self.action_details['action_description']}, Location')

    def _location_move_actions(self) -> None:
        """
        Generates move actions for the Action List based on the possible moves of the current location.
        Each move action is added to the action list.
        """
        for self.key, self.move in self.location.location_possible_moves.items():
            self.newActionReference = ActionReference(
                self.move.id, self.move.name, self.move.description, 'MoveLocation')
            self.action_reference_list.append(self.newActionReference)

    def _player_actions(self) -> None:
        """
        Retrieves the actions associated with the player items and adds them to the action list.

        Returns:
            None
        """
        self.player_items = self.player.player_items
        for self.player_item in self.player_items:
            if self.player_item.actions:
                for action_name, action_details in self.player_item.actions.items():
                    new_action_reference = ActionReference(
                        action_details['action_id'], action_name, action_details['action_description'], 'Player')
                    self.action_reference_list.append(new_action_reference)

    def create_action_reference_list(self):
        """
        Creates the action reference list for the current location and player.
        The action reference list is a list of ActionReference objects that represent 
        the actions available to the player at the current location.
        Returns:
            None
        """
        self._clear_action_reference_list()
        self._location_actions()
        self._location_move_actions()
        self._player_actions()

    def get_list_of_action_descriptions_by_type(self, action_type: str) -> list:
        """
        Returns a list of strings describing actions of a specific type available to the player at the current location.
        Using the action_reference_list, the function extracts the action descriptions where the action type matches the given type.
        """
        actions = []
        for action_ref in self.action_reference_list:
            if action_ref.action_type == action_type:
                actions.append(action_ref.description)
        return actions

    def get_list_of_location_action_descriptions(self) -> list:
        """
        Returns a list of strings describing available actions (excluding move actions) to the player at the current location.
        """
        return self.get_list_of_action_descriptions_by_type('Location')

    def get_list_of_move_action_descriptions(self) -> list:
        """
        Returns a list of strings describing available move actions to the player at the current location.
        """
        return self.get_list_of_action_descriptions_by_type('MoveLocation')

    def get_list_of_player_action_descriptions(self) -> list:
        """
        Returns a list of strings describing available player actions to the player at the current location.
        """
        return self.get_list_of_action_descriptions_by_type('Player')

    def _clear_action_reference_list(self) -> None:
        """
        Clears the action reference list.
        """
        self.action_reference_list.clear()
        self.logger.debug('Action reference list cleared')

    def get_item_id_for_action_description(self, action_description: str) -> str:
        """
        Retrieves the item_id based on the given action description.
        """
        for action_ref in self.action_reference_list:
            if action_ref.description == action_description:
                return action_ref.id
        return None
