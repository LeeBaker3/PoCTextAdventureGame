import xml.etree.ElementTree as ET


class Location:
    """_summary_
    """

    def __init__(self, id: str, name: str, description: str, items: list[str], possible_moves: dict):
        self.location_id = id
        self.location_name = name
        self.location_description = description
        self.location_items = items
        self.location_possible_moves = possible_moves

    @property
    def movesLength(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return len(self.location_possible_moves)

    @property
    def itemsLength(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return len(self.location_items)


class LoadLocations:
    """_summary_
    """

    def __init__(self, locations: dict, file_path: str):
        """_summary_

        Args:
            locations (_type_): _description_
            file_path (_type_): _description_
        """
        self.locations = locations
        self.file_path = file_path

    def load(self):
        """_summary_
        """

        self.tree = ET.parse(self.file_path)
        self.root = self.tree.getroot()

        self.locationLen = len(self.root.findall("location"))

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
                    self.destination_location_ids[self.move.get(
                        'destination_location_id')] = self.move.text

            self.newLocation = Location(
                self.location_id, self.location_name, self.location_description, self.item_ids, self.destination_location_ids)
            self.locations[self.location_id] = self.newLocation

    def locations(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        return self.locations
