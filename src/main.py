# import player
# import location

from player import Player
from item import Item
from item import LoadItems
from locations import Location
from locations import LoadLocations

import config
import os
import openai

# cwd = os.getcwd()
# print("Current working directory:", cwd)


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

    # Prints movelist for development purposes. Needs to be removed.
    print(moveList)

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

    itemsLen = currentLocation.itemsLength()

    itemList = 'A '
    if itemsLen == 1:
        itemList = itemList + items[currentLocation.items[0]].item_name
    else:
        for item in enumerate(currentLocation.items):
            if item in {0, itemsLen-1}:
                itemList = 'and ' + items[str(item)].item_name
            else:
                itemList = ', ' + items[str(item)].item_name

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
        {"role": "system", "content": "From the user input, determine what the user requested from the possible actions available."},
        {"role": "user",
            "content": f"Possible actions: {', '.join(possibleActions)}. User input: {playerInput}"}
    ]
    print(messages)
    # Get ChatGPT's response to determine the move
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use ChatGPT-3.5
        messages=messages,
        max_tokens=10,  # Set to 10. This should be enough to determine the action chosen
        api_key=api_key
    )

    # Get the move recommended by ChatGPT-3.5
    action = response.choices[0].message['content'].strip()
    return action


currentLocation = locations['1']
health = 100

# while health>0:

print(currentLocation.location_description)
movesMessage(currentLocation)
itemsMessage(currentLocation, items)

playerInput = input(start + "What would you like to do? :" + end)
possibleMoves = currentLocation.possibleMoves.values()
print(possibleMoves)
userAction = determineUserInput(possibleMoves, playerInput)
print("You choose to: {}".format(userAction))

