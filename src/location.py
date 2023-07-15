import xml.etree.ElementTree as ET


class Location:

    def __init__(self, name, description, possibleMoves):
        self.name = name
        self.description = description
        self.items = [None]
        self.possibleMoves = [None]


class LoadLocations:

    def __init__(self, locations, filePath):
        self.locations = locations
        self.filePath = filePath

    def load(self):
        
        self.tree = ET.parse(self.filePath)
        self.root = self.tree.getroot()
        
        print("Element Tree")
        
        self.locationLen = len(self.root.findall("location"))
        print("There are {0} locations".format(self.locationLen))
        
        for self.child in self.root:
            self.location_name = self.child.find('location_name')
            self.location_description = self.child.find('location_description')
            self.items = self.child.find('items')
            self.moves = self.child.find('moves')
            self.item_ids = []
            self.destination_location_ids = {}
            
            
            self.itemsLen = len(self.items.findall("item"))
            if self.itemsLen > 0:
                for self.item in self.items:
                    self.item_ids.append(self.item.attrib)
                          
            
            self.movesLen = len(self.moves.findall("move"))
            if self.movesLen > 0:
                for self.move in self.moves:
                    self.destination_location_ids[self.move.text] = self.move.text

            
            print(self.child.tag, self.child.attrib)
            print(self.location_name.text)
            print(self.location_description.text)
            print("There are {0} items".format(self.itemsLen))
            print([x for x in self.item_ids])
            
            print("There are {0} moves\n".format(self.movesLen))
            print([x for x in self.destination_location_ids])


    def locations(self):
        return self.locations
        return self.locations
