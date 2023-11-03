# import player
# import location
from player import Player
from location import Location
from location import LoadLocations
from item import Item
from item import LoadItems

locations = {}
loadLocations = LoadLocations(locations, "locations.xml")
loadLocations.load()

items = {}
loadItems = LoadItems(items, "items.xml")
loadItems.load()


welcome = 'Welcome to your greatest adventure'
introduction = 'We are going on an adventure. But first, make sure your parents know {0}! Remember, never go on adventures with strangers\n'

print(welcome)
playerName = input("What is your name adventurer?")
player = Player(playerName=playerName)

print('Hello {0}'.format(player.name()))
print(introduction.format(player.name()))


def movesMessage(currentLocation):
    moves = currentLocation.movesLength()
    if moves > 1:
        moveMessage = 'There are {0} possible moves'
    else:
        moveMessage = 'There is {0} possible move'
    print(moveMessage.format(moves))


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


currentLocation = locations['1']
health = 100

# while health>0:

print(currentLocation.location_description)
movesMessage(currentLocation)
itemsMessage(currentLocation, items)
