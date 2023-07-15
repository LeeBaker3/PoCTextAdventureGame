# import player
# import location
from player import Player
from location import Location
from location import LoadLocations

welcome = 'Welcome to your greatest adventure'
introduction = 'We are going on an adventure. But first, make sure your parents know {0}! Remember, never go on adventures with strangers'

print(welcome)

playerName = input("What is your name adventurer?")

player = Player(playerName=playerName)


locations = {}
loadLocations = LoadLocations(locations, "locations.xml")
loadLocations.load()

print('Hello {0}'.format(player.name()))

print(introduction.format(player.name()))

health = 100

# while health>0:
