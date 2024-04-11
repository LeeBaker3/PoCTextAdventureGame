import sys
import logging
import time
from src.action_list_manager import ActionListManager
from src.action_factory import ActionFactory
import src.config as config
from logging import Logger
from src.player.player import Player
from src.items.item import Item
from src.items.item import LoadItems
from src.locations.location import LoadLocations, Location
from src.item_list import ItemList
from openai import OpenAI
from pathlib import Path
from typing import List

file_path = Path(__file__).parent


def load_game_config() -> tuple[dict, dict]:
    """
    Loads the game configuration from the specified files and returns a tuple containing
    the locations and items dictionaries.

    Returns:
        tuple[dict, dict]: A tuple containing the locations and items dictionaries.
    """
    config_folder_path = file_path / config.game_config['game_config_folder']
    items_config_file = config_folder_path / config.game_config['items_config']
    locations_config_file = config_folder_path / \
        config.game_config['locations_config']

    locations = {}  # locations (Dictionary): Holds the game location objects
    load_locations = LoadLocations(
        locations, locations_config_file)
    load_locations.load()

    items = {}  # items (Dictionary): Holds the game item objects
    load_items = LoadItems(items, items_config_file)
    load_items.load()

    return (locations, items)


def game_start() -> Player:
    pass


def game_exit() -> None:
    """
    Exits the game.
    """
    player_output(True, "You've chosen to exit the game")
    sys.exit()


def bold_string(msg: str) -> str:
    """
    Formats the given string to be displayed as bold text.

    Args:
        msg (str): The string to be formatted.

    Returns:
        str: The formatted string with bold text.
    """
    start = '\033[1m'  # Bold text
    end = '\033[0;0m'  # Normal text
    return f'{start}{msg}{end}'


def player_output(bold: bool, msg: str) -> None:
    """
    Prints the given player output message with optional bold formatting.

    This function could be modified to output to other sources such as text box in a UI.

    Args:
        bold (bool): Indicates whether the message should be printed in bold.
        msg (str): The message to be printed.

    Returns:
        None
    """
    if bold == True:
        msg = bold_string(msg)
    print(msg)


def player_input(bold: bool, msg: str) -> str:
    """
    Displays a message and takes user input and returns it as a string.

    Args:
        bold (bool): Indicates whether the message should be displayed in bold.
        msg (str): The message to be displayed to the user.

    Returns:
        str: The user's input as a string.
    """
    if bold == True:
        msg = bold_string(msg)
    return input(msg)


def create_logger() -> Logger:
    """
    Create and configure a logger object.

    Returns:
        Logger: The configured logger object.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(config.logging['level'])

    formatter = logging.Formatter(
        "%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(config.logging['log_file'])
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.info("Logger created\n.")
    return logger


def player_input_exit(user_input: str) -> bool:
    """
    Checks if the user input is 'exit'.

    Args:
        user_input (str): The user input to check.

    Returns:
        bool: True if the user input is 'exit', False otherwise.
    """
    if user_input.lower() == 'exit':
        return True
    return False


def create_moves_message(location: Location, logger: Logger) -> str:
    '''Summary or Description of the Function
    This function take a Location object and generates a message
    describing the number of available moves in the  location and
    what those moves are.

    Parameters:
    Location (obj): instance of the location.py object that is
    current in-scope location
   '''

    # movesLen (Integer): The number of possible moves at the current location
    moves_len = location.moves_length

    # moveList (string): An empty string that will hold the possible move
    # descriptions
    move_list = ''

    # Populate the empty moveList (string) with move descriptions from the
    # currentLocation location (object).
    for move in location.location_possible_moves.values():
        move_list = move_list + '\n- ' + move.description

    # Logs movelist for debug purposes.
    logger.debug('Move list: {}'.format(move_list))

    # Build the moveMessage that is output to the the player. The if/else
    # statement determines if there is 1 or more moves from the
    # movesLen (integer) and builds the message for a either a single, or
    # multiple moves.
    if moves_len > 1:
        move_message = 'There are {0} possible moves. . ' + move_list
    else:
        move_message = 'There is {0} possible move. . ' + move_list
    return move_message.format(moves_len)


def create_location_items_message(location: Location, items: dict, logger: Logger) -> str:
    '''Summary or Description of the Function
    This function take a Location object and generates a message
    describing the number of available items in the location and what
    those items are.

    Parameters:
    Location (obj): instance of the location.py object that is current
    in-scope location
   '''

    # itemsLen (Integer): The number of items at the current location
    items_len = location.items_length

    # itemList (string): A string that will hold the item descriptions
    item_list = ''

    # Populate the itemList (string) with item descriptions from the
    # currentLocation location (object).
    for item, (value) in enumerate(location.location_items):
        item_list = item_list + '\n- ' + items[str(value)].item_name

    # Build the itemsMessage that is output to the the player. The if/else
    # statement determines if there is 1 or more items from the
    # itemsLen (integer) and builds the message for a either a single, or
    # multiple items.
    if items_len == 0:
        items_message = 'There are no items here '
    elif items_len == 1:
        items_message = 'There is {0} item here. ' + item_list
    else:
        items_message = 'There are {0} items here. ' + item_list
    return items_message.format(items_len)


def create_user_items_message(player: Player, logger: Logger) -> str:
    """
    Prints a message indicating the items the player is currently carrying.

    Args:
        player (Player): The player object.
        logger (Logger): The logger object.

    Returns:
        None
    """

    item_list = ''
    if player.player_items_length > 0:
        for item in player.player_items:
            item_list = item_list + '\n- ' + item.item_name
            item_message = f'You are currently carrying: {item_list}'
    else:
        item_message = f'You are not currently carrying any items'
    return item_message


def determine_user_input(available_actions: List[str], player_input: str, logger: Logger) -> str:
    """Function to interact with ChatGPT and determine the move

    Parameters:
    possibleActions (array): A list of the current possible actions/moves
    playerInput (string): Text string input by the player requesting what
    action/move the player wants to execute.
   """

    # Define your OpenAI API key
    api_key = config.openai['api_key']
    client = OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": "From the user input, determine what the user requested from the possible actions available. Only return the text of the matching possible action. Otherwise return no match"},
        {"role": "user",
            "content": f"Possible actions: {', '.join(available_actions)}. User input: {player_input}"}
    ]
    logger.debug(f'ChatGPT API message: {messages}')
    logger.debug(f'possibleActions: {available_actions}')
    logger.debug(f'Player input: {player_input}')

    # Get ChatGPT's response to determine the move
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use ChatGPT-3.5
                                              messages=messages,
                                              max_tokens=20)  # Set to 20. This should be enough to determine the action chosen

    # Get the move recommended by ChatGPT-3.5
    action = response.choices[0].message.content.strip()
    return action


def search_possible_moves(user_action: str, possible_moves: dict, logger: Logger) -> str:
    result = [key for key, move in possible_moves.items() if move.description ==
              user_action]
    logger.debug(f'possible_moves: {possible_moves.items()}')
    logger.debug(f'result: {result}')
    if result:
        return result[0]
    return None


def perform_action(user_action: str, action: str, current_location: Location, locations: dict, items: dict, item: Item, player: Player, logger: Logger) -> 'Location':

    actionFactory = ActionFactory()
    currentAction = actionFactory.create(
        action, player, current_location, locations, item, items, logger, user_action)
    success, player_msg = currentAction.action()
    if success == True:
        return player_msg, *currentAction.return_game_state()

    else:
        return player_msg, current_location, locations, items, item, player


def main():
    logger = create_logger()
    logger.info("App started\n.")

    locations, items = load_game_config()

    welcome_msg = 'Welcome to your greatest adventure.'
    player_output(False, welcome_msg)

    player_name_msg = 'What is your name adventurer? : '
    player_name = player_input(True, player_name_msg)

    player = Player(player_name=player_name)

    current_location = locations['0']
    health = 10

    if player_input_exit(player_name) == False:
        player_hello_msg = f'\nHello {player_name}'
        player_output(False, player_hello_msg)

        introduction_msg = ('We are going on an adventure. But first, make sure your '
                            f'parents know {player_name}! Remember, never go on adventures with strangers\n')
        player_output(False, introduction_msg)

    else:
        game_exit()

    while health > 0:

        current_location_description = current_location.location_description
        player_output(False, current_location_description)
        move_message = create_moves_message(
            location=current_location, logger=logger)
        player_output(False, move_message)
        location_message = create_location_items_message(location=current_location,
                                                         items=items, logger=logger)
        player_output(False, location_message)
        user_items_message = create_user_items_message(
            player=player, logger=logger)
        player_output(False, user_items_message)

        player_instructions = player_input(
            True, f'\nWhat would you like to do? : ')
        if player_input_exit(player_instructions) is False:

            action_list_manager = ActionListManager(
                current_location, player, items, locations, logger)
            action_list_manager.create_action_reference_list()
            available_moves = action_list_manager.get_list_of_move_action_descriptions()
            available_actions = action_list_manager.get_list_of_location_action_descriptions()
            available_actions.extend(
                action_list_manager.get_list_of_player_action_descriptions())

            action_description = determine_user_input(
                available_actions=(available_actions + available_moves),
                player_input=player_instructions, logger=logger)
            item_id = action_list_manager.get_item_id_for_action_description(
                action_description=action_description)
            if item_id is not None:  # Fix: Added colon after "not"
                item = items[item_id]
            else:
                item = None
            action = action_list_manager.get_action_name_by_action_description(
                action_description=action_description)
            player_output(False, f"\nYou choose to: {action_description}")

            player_msg, player, current_location, locations, item, items = perform_action(
                user_action=action_description, action=action, current_location=current_location, locations=locations, items=items, item=item,
                player=player, logger=logger)

            player_output(True, player_msg)

            health = health - 1
        else:
            health = 0
            game_exit()

        player_output(False, f"\nYour health is {health}\n")


if __name__ == "__main__":
    main()
