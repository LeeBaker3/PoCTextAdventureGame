class Player():

    def __init__(self, player_name):
        self.player_name = player_name
        self.items = [None]

    def name(self):
        return self.player_name

    def add_items(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def items(self):
        return self.items
