import sys
import logging
import time
import src.config as config
from src.player.player import Player
from logging import Logger
from src.items.item import Item
from src.items.item import LoadItems
from src.locations.location import LoadLocations, Location
from src.item_list import ItemList
from openai import OpenAI
from pathlib import Path
from typing import List

file_path = Path(__file__).parent


def load_game_config() -> tuple[dict, dict]:
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
    pass


def bold_string(msg: str) -> str:
    start = '\033[1m'  # Bold text
    end = '\033[0;0m'  # Normal text
    return f'{start}{msg}{end}'


def player_output(bold: bool, msg: str) -> None:
    if bold == True:
        msg = bold_string(msg)
    print(msg)


def player_input(bold: bool, msg: str) -> str:
    if bold == True:
        msg = bold_string(msg)
    return input(msg)


def create_logger() -> Logger:
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
    '''Summary or Description of the Function
    Check is the user has chosen to exit the game.
    If they have chosen to Exit the function will return True.
    Otherwise it returns false.
    '''

    if user_input.lower() == 'exit':
        return True
    return False


def moves_message(location: Location, logger: Logger) -> None:
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
    for key, value in location.location_possible_moves.items():
        move_list = move_list + '\n- ' + value

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
    print(move_message.format(moves_len))


def location_items_message(location: Location, items: dict, logger: Logger) -> None:
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
    print(items_message.format(items_len))


def user_items_message(player: Player, logger: Logger) -> None:
    """_summary_

    Args:
        player (Player): _description_
        logger (Logger): _description_
    """

    item_list = ''
    if player.player_items_length > 0:
        for item in player.player_items:
            item_list = item_list + '\n- ' + item.item_name
            item_message = f'You are currently carrying: {item_list}'
    else:
        item_message = f'You not currently carrying any items'
    print(item_message)


def create_available_actions(location: Location, player: Player, items: List[Item], logger: Logger) -> List[str]:
    """_summary_

    Returns:
        _type_: _description_
    """
    available_actions = []

    for item, (value) in enumerate(location.location_items):
        actions = items[str(value)].actions.items()
        logger.debug('Action list for {items[str(value)].item_description}: '
                     f'{actions} total actions: {len(actions)}')

        for action in actions:
            _, action_details = action
            if action_details['holding'] == 'No':
                available_actions.append(action_details['action_description'])
            else:
                pass

            logger.debug(f'Available actions {available_actions}')
    return available_actions


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
    result = [key for key, value in possible_moves.items() if value ==
              user_action]
    logger.debug(f'possible_moves: {possible_moves.items()}')
    logger.debug(f'result: {result}')
    if result:
        return result[0]
    return None


def main():
    logger = create_logger()
    logger.info("App started\n.")

    locations, items = load_game_config()

    welcome_msg = 'Welcome to your greatest adventure.'
    player_output(False, welcome_msg)

    player_name_msg = 'What is your name adventurer? : '
    player_name = player_input(True, player_name_msg)

    player = Player(player_name=player_name)

    if player_input_exit(player_name) == False:
        player_hello_msg = f'\nHello {player_name}'
        player_output(False, player_hello_msg)

        introduction_msg = ('We are going on an adventure. But first, make sure your '
                            f'parents know {player_name}! Remember, never go on adventures with strangers\n')
        player_output(False, introduction_msg)

    else:
        sys.exit()

    current_location = locations['0']
    health = 10

    while health > 0:

        print(current_location.location_description)
        moves_message(location=current_location, logger=logger)
        location_items_message(location=current_location,
                               items=items, logger=logger)
        user_items_message(player=player, logger=logger)

        player_instructions = player_input(
            True, f'\nWhat would you like to do? : ')
        if player_input_exit(player_instructions) is False:
            available_moves = list(
                current_location.location_possible_moves.values())
            available_actions = create_available_actions(
                location=current_location, player=player, items=items, logger=logger)

            user_action = determine_user_input(
                available_actions=(available_actions + available_moves), player_input=player_instructions, logger=logger)

            player_output(False, f"\nYou choose to: {user_action}")

            new_location_key = search_possible_moves(
                user_action=user_action, possible_moves=current_location.location_possible_moves, logger=logger)

            if new_location_key != None:

                logger.debug(f"key Value for new location: {new_location_key}")
                current_location = locations[new_location_key[0]]
            else:
                player_output(
                    True, f"That doesn't match any of the possible actions")
                time.sleep(2)

            health = health - 1
        else:
            health = 0
            player_output(False, "You've chosen to exit the game")

        player_output(False, f"\nYour health is {health}\n")


if __name__ == "__main__":
    main()
