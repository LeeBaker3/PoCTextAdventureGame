class Player():

    def __init__(self, playerName):
        self.playerName = playerName
        self.items = [None]

    def name(self):
        return self.playerName

    def add_items(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def items(self):
        return self.items
