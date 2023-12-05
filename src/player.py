class Player():
    
    def __init__(self, playerName):
        self.playerName = playerName
        self.items = [None]
    
    def name(self):
        return self.playerName
    
    def addItems(self, item):
        self.items.append(item)
        
    def removeItem(self, item):
        self.items.remove(item) 
    
    def items(self):
        return self.items
        