# import player
# import location

import sys
import logging
import time
import config
from player import Player
from item import Item
from item import LoadItems
from locations.location import LoadLocations, Location
from item_list import ItemList
from openai import OpenAI

# Define your OpenAI API key
api_key = config.openai['api_key']
client = OpenAI(api_key=api_key)

logger = logging.getLogger(__name__)
logger.setLevel(config.logging['level'])

formatter = logging.Formatter(
    "%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")

file_handler = logging.FileHandler(config.logging['log_file'])
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info("App started\n.")


locations = {}  # locations (Dictionary): Holds the game location objects
load_locations = LoadLocations(locations, "game_config/locations.xml")
load_locations.load()


items = {}  # items (Dictionary): Holds the game item objects
load_items = LoadItems(items, "game_config/items.xml")
load_items.load()

item_list = ItemList()
item_list.maxListLength = 3


def user_input_exit(user_input: str) -> bool:
    '''Summary or Description of the Function
    Check is the user has chosen to exit the game.
    If they have chosen to Exit the function will return True.
    Otherwise it returns false.
    '''

    if user_input.lower() == 'exit':
        return True
    return False


def moves_message(current_location: Location) -> None:
    '''Summary or Description of the Function
    This function take the currentLocation object and generates a message
    describing the number of available moves in the current location and
    what those moves are.

    Parameters:
    currentLocation (obj): instance of the location.py object that is
    current in-scope location
   '''

    # movesLen (Integer): The number of possible moves at the current location
    moves_len = current_location.movesLength

    # moveList (string): An empty string that will hold the possible move
    # descriptions
    move_list = ''

    # Populate the empty moveList (string) with move descriptions from the
    # currentLocation location (object).
    for key, value in current_location.location_possible_moves.items():
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


def items_message(current_location: Location, items: dict) -> None:
    '''Summary or Description of the Function
    This function take the currentLocation object and generates a message
    describing the number of available items in the current location and what
    those items are.

    Parameters:
    currentLocation (obj): instance of the location.py object that is current
    in-scope location
   '''

    # itemsLen (Integer): The number of items at the current location
    items_len = current_location.itemsLength

    # itemList (string): A string that will hold the item descriptions
    item_list = ''

    # Populate the itemList (string) with item descriptions from the
    # currentLocation location (object).
    for item, (value) in enumerate(current_location.location_items):
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


def determine_user_input(possible_actions, player_input):
    '''Function to interact with ChatGPT and determine the move

    Parameters:
    possibleActions (array): A list of the current possible actions/moves
    playerInput (string): Text string input by the player requesting what
    action/move the player wants to execute.

   '''
    messages = [
        {"role": "system", "content": "From the user input, determine what the user requested from the possible actions available. Only return the text of the matching possible action. Otherwise return no match"},
        {"role": "user",
            "content": f"Possible actions: {', '.join(possible_actions)}. User input: {player_input}"}
    ]
    logger.debug(f'ChatGPT API message: {messages}')
    logger.debug(f'possibleActions: {possible_actions}')
    logger.debug(f'Player input: {player_input}')

    # Get ChatGPT's response to determine the move
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use ChatGPT-3.5
                                              messages=messages,
                                              max_tokens=20)  # Set to 20. This should be enough to determine the action chosen

    # Get the move recommended by ChatGPT-3.5
    action = response.choices[0].message.content.strip()
    return action


def search_possible_moves(user_action, possible_moves):
    result = [key for key, value in possible_moves.items() if value ==
              user_action]
    logger.debug(f'possible_actions: {possible_moves.items()}')
    logger.debug(f'result: {result}')
    if result:
        return result[0]
    return None


start = '\033[1m'  # Bold text
end = '\033[0;0m'  # Normal text


welcome = 'Welcome to your greatest adventure'
introduction = 'We are going on an adventure. But first, make sure your '\
    'parents know {0}! Remember, never go on adventures with strangers\n'

print(welcome)
player_name = input('{}{}{}'.format(
    start, 'What is your name adventurer? :', end))

if user_input_exit(player_name) == False:

    player = Player(playerName=player_name)

    print('\nHello {}'.format(player.name()))
    print(introduction.format(player.name()))
else:
    sys.exit()


current_location = locations['0']
health = 10

while health > 0:

    print(current_location.location_description)
    moves_message(current_location)
    items_message(current_location, items)

    player_input = input(start + "\nWhat would you like to do? :" + end)
    if user_input_exit(player_input) is False:
        possible_moves = current_location.location_possible_moves.values()

        user_action = determine_user_input(possible_moves, player_input)

        print("\nYou choose to: {}".format(user_action))

        new_location_key = search_possible_moves(
            user_action, current_location.location_possible_moves)

        if new_location_key != None:

            logger.debug(
                "key Value for new location: {}".format(new_location_key))
            current_location = locations[new_location_key[0]]
        else:
            print("{}That doesn't match any of the possible actions{}".format(start, end))
            time.sleep(2)

        health = health - 1
    else:
        health = 0
        print("You've chosen to exit the game")

    print("\nYour health is {}\n".format(health))
