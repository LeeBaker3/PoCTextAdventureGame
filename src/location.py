from bs4 import BeautifulSoup

class Location:
    
    def __init__(self, name, description, possibleMoves):
        self.name = name
        self.description = description
        self.items = [None]
        self.possibeMoves = [None]

class LoadLocations:
    
    def __init__(self, locations, filePath):
        self.locations = locations
        self.filePath = filePath
        
    def load(self):
        with open(self.filePath, 'r', encoding="utf-8") as f:
            self.file = f.read()
        self.soup = BeautifulSoup(self.file, 'xml')
        
        self.locationLen = len(self.soup.find_all("location"))
        print("There are {0} locations".format(self.locationLen))
        
    
    def locations(self):
        return self.locations
    
    
    
    