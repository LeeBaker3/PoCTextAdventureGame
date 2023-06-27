class Location:
    
    def __init__(self, name, description, possibleMoves):
        self.name = name
        self.description = description
        self.items = [None]
        self.possibeMoves = [None]

class LoadLocations:
    
    def __init__(self, locations):
        self.locations = locations
        
    def load(self):
        pass
    
    def locations(self):
        return self.locations
    
    
    
    