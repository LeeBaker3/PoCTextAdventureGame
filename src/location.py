import xml.etree.ElementTree as ET


class Location:
    """_summary_
    """

    def __init__(self, id, name, description, items, possibleMoves):
        self.location_id = id
        self.location_name = name
        self.location_description = description
        self.items = items
        self.possibleMoves = possibleMoves

    def movesLength(self):
        return len(self.possibleMoves)

    def itemsLength(self):
        return len(self.items)


class LoadLocations:
    """_summary_
    """

    def __init__(self, locations, filePath):
        self.locations = locations
        self.filePath = filePath

    def load(self):
        """_summary_
        """

        self.tree = ET.parse(self.filePath)
        self.root = self.tree.getroot()

        print("Element Tree")

        self.locationLen = len(self.root.findall("location"))
        print("There are {0} locations".format(self.locationLen))

        for self.child in self.root:
            self.location_id = self.child.attrib['location_id']
            self.location_name = self.child.find('location_name').text
            self.location_description = self.child.find(
                'location_description').text
            self.items = self.child.find('items')
            self.moves = self.child.find('moves')

            self.item_ids = []
            self.itemsLen = len(self.items.findall("item"))
            if self.itemsLen > 0:
                for self.item in self.items:
                    self.item_ids.append(self.item.get('item_id'))

            self.destination_location_ids = {}
            self.movesLen = len(self.moves.findall("move"))
            if self.movesLen > 0:
                for self.move in self.moves:
                    # print('move attribut{0}'.format(
                    #   self.move.get('destination_location_id')))
                    self.destination_location_ids[self.move.get(
                        'destination_location_id')] = self.move.text

            self.newLocation = Location(
                self.location_id, self.location_name, self.location_description, self.item_ids, self.destination_location_ids)
            self.locations[self.location_id] = self.newLocation

            '''
            print(self.child.tag, self.child.attrib)
            print(self.location_name.text)
            print(self.location_description.text)
            print("There are {0} items".format(self.itemsLen))
            print([x for x in self.item_ids])
            
            print("There are {0} moves\n".format(self.movesLen))
            print([x for x in self.destination_location_ids])
            '''

    def locations(self):
        return self.locations
