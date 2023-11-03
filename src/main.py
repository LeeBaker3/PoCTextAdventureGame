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

#cwd = os.getcwd()
#print("Current working directory:", cwd)


locations = {}
loadLocations = LoadLocations(locations, "locations.xml")
loadLocations.load()

items = {}
loadItems = LoadItems(items, "items.xml")
loadItems.load()

start = '\033[1m' #Bold text
end = '\033[0;0m' #Normal text


welcome = 'Welcome to your greatest adventure'
introduction = 'We are going on an adventure. But first, make sure your parents know {0}! Remember, never go on adventures with strangers\n'

print(welcome)
playerName = input('{}{}{}'.format(start, 'What is your name adventurer? :', end))
player = Player(playerName=playerName)

print('\nHello {0}'.format(player.name()))
print(introduction.format(player.name()))


def movesMessage(currentLocation):
	moveslen = currentLocation.movesLength()
	
	currentLocation.possibleMoves.items()
	moveList = ''
	
	for key, value in currentLocation.possibleMoves.items():
		moveList = moveList + ' ' + value
		
		
	print (moveList)
	
	if moveslen > 1:
		moveMessage = 'There are {0} possible moves' + moveList
	else:
		moveMessage = 'There is {0} possible move' + moveList
	print(moveMessage.format(moveslen))
	
	
def itemsMessage(currentLocation, items):

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

print('API key:' + api_key)

# Function to interact with ChatGPT and determine the move
def determineUserInput(possibleActions, playerInput):
	# Create a prompt that includes the possible moves and user input
	# Create a system message and a user message with possible moves and user input
	messages = [
	{"role": "system", "content": "You are a text-based adventure game character."},
	{"role": "user", "content": f"Possible actions: {', '.join(possibleActions)}. User input: {playerInput}"}
	]
	print(messages)
	# Get ChatGPT's response to determine the move
	response = openai.ChatCompletion.create(
	model="gpt-3.5-turbo",  # Use ChatGPT-3.5
	messages=messages,
	max_tokens=1,  # Set to 1 to get a single word response
	api_key=api_key
	)
	
	action = response.choices[0].message['content'].strip()  # Get the move recommended by ChatGPT-3.5
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
print ("You choose to: {}".format(userAction))

