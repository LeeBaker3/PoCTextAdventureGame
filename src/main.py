# import player
# import location

from player import Player
from item import Item
from item import LoadItems
from location.locations import Location, LoadLocations
# from location.locations import LoadLocations

import config
import openai
import logging

logger = logging.getLogger(__name__)
logger.setLevel(config.logging['level'])

formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")

file_handler = logging.FileHandler(config.logging['log_file'])
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info("App started\n.")


locations = {}  # locations (Dictonary): Holds the game location objects
loadLocations = LoadLocations(locations, "locations.xml")
loadLocations.load()

items = {}  # items (Dictonary): Holds the game item objects
loadItems = LoadItems(items, "items.xml")
loadItems.load()

start = '\033[1m'  # Bold text
end = '\033[0;0m'  # Normal text


welcome = 'Welcome to your greatest adventure'
introduction = 'We are going on an adventure. But first, make sure your '\
    'parents know {0}! Remember, never go on adventures with strangers\n'

print(welcome)
playerName = input('{}{}{}'.format(
    start, 'What is your name adventurer? :', end))
player = Player(playerName=playerName)

print('\nHello {0}'.format(player.name()))
print(introduction.format(player.name()))


def movesMessage(currentLocation):
    '''Summary or Description of the Function
    This function take the currentLocation object and generates a message
    desribing the number of available moves in the current location and
    what those moves are.

    Parameters:
    currentLocation (obj): instance of the location.py object that is
    current in-scope location
   '''

    # movesLen (Integer): The number of possible moves at the current location
    movesLen = currentLocation.movesLength()

    # moveList (string): An empty string that will hold the possible move
    # descriptions
    moveList = ''

    # Populate the empty moveList (string) with move descriptions from the
    # currentLocation location (object).
    for key, value in currentLocation.possibleMoves.items():
        moveList = moveList + ' ' + value

    # Logs movelist for debug purposes.
    logger.debug('Move list: {}'.format(moveList))

    # Build the moveMessage that is output to the the player. The if/else
    # statement determines if there is 1 or more moves from the
    # movesLen (integer) and builds the message for a either a single, or
    # multiple moves.
    if movesLen > 1:
        moveMessage = 'There are {0} possible moves' + moveList
    else:
        moveMessage = 'There is {0} possible move' + moveList
    print(moveMessage.format(movesLen))


def itemsMessage(currentLocation, items):
    '''Summary or Description of the Function
    This function take the currentLocation object and generates a message
    desribing the number of available items in the current location and what
    those items are.

    Parameters:
    currentLocation (obj): instance of the location.py object that is current
    in-scope location
   '''

    # itemsLen (Integer): The number of items at the current location
    itemsLen = currentLocation.itemsLength()

    # itemList (string): A string that will hold the item descriptions
    itemList = 'A '

    # Populate the itemList (string) with item descriptions from the
    # currentLocation location (object).
    if itemsLen == 1:
        itemList = itemList + items[currentLocation.items[0]].item_name
    else:
        for item in enumerate(currentLocation.items):
            if item in {0, itemsLen-1}:
                itemList = 'and ' + items[str(item)].item_name
            else:
                itemList = ', ' + items[str(item)].item_name

    # Build the itemsMessage that is output to the the player. The if/else
    # statement determines if there is 1 or more items from the
    # itemsLen (integer) and builds the message for a either a single, or
    # multiple items.
    if itemsLen == 0:
        itemsMessage = 'There are no items here '
    elif itemsLen == 1:
        itemsMessage = 'There is {0} item here. ' + itemList
    else:
        itemsMessage = 'There are {0} items here. ' + itemList
    print(itemsMessage.format(itemsLen))


# Define your OpenAI API key
api_key = config.openai['api_key']


def determineUserInput(possibleActions, playerInput):
    '''Function to interact with ChatGPT and determine the move

    Parameters:
    possibleActions (array): A list of the current possible actions/moves
    playerInput (string): Text string input by the player requesting what
    action/move the player wants to execute.

   '''
    messages = [
        {"role": "system", "content": "From the user input, determine what the user requested from the possible actions available. Only return the text of the matching possible action. Otherwise return no match"},
        {"role": "user",
            "content": f"Possible actions: {', '.join(possibleActions)}. User input: {playerInput}"}
    ]
    logger.debug('ChatGPT API message:'.format(messages))

    # Get ChatGPT's response to determine the move
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use ChatGPT-3.5
        messages=messages,
        max_tokens=20,  # Set to 20. This should be enough to determine the action chosen
        api_key=api_key
    )

    # Get the move recommended by ChatGPT-3.5
    action = response.choices[0].message['content'].strip()
    return action


def searchPossibleMoves(userAction, possibleMoves):
    result = [key for key, value in possibleMoves.items() if value ==
              userAction]
    # print("Result: {} Type: {} and Length: {}".format(
    #    str(result), type(result), len(result)))
    if result:
        return result[0]
    return None


currentLocation = locations['0']
health = 10

while health > 0:

    print(currentLocation.location_description)
    movesMessage(currentLocation)
    itemsMessage(currentLocation, items)

    playerInput = input(start + "What would you like to do? :" + end)
    if playerInput.lower() != "exit":
        possibleMoves = currentLocation.possibleMoves.values()

        userAction = determineUserInput(possibleMoves, playerInput)

        print("You choose to: {}".format(userAction))
        # print("Possible moves type: {}".format(currentLocation.possibleMoves))

        newLocationKey = searchPossibleMoves(
            userAction, currentLocation.possibleMoves)

        if newLocationKey != None:

            logger.debug(
                "key Value for new location: {}".format(newLocationKey))
            currentLocation = locations[newLocationKey[0]]
        else:
            print("That doesn't match any of the possible actions")

        health = health - 1
    else:
        health = 0
        print("you choose to exit the game")

    print("health: {}".format(health))
