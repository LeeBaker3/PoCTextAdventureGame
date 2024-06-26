import xml.etree.ElementTree as ET
from dataclasses import dataclass, field


@dataclass
class Move:
    """
    Represents a move in the game.

    Attributes:
        id (str): The unique identifier of the move.
        name (str): The name of the move.
        description (str): The description of the move.
        destination_location_id (str): The identifier of the destination location.
    """
    id: str
    name: str
    description: str
    destination_location_id: str


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
    def moves_length(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return len(self.location_possible_moves)

    @property
    def items_length(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return len(self.location_items)


class LoadLocations:
    """_summary_
    """

    def __init__(self, locations: dict, file_path: str):
        """Initialize a Location object.

        Args:
            locations (dict): A dictionary containing information about different locations.
            file_path (str): The file path of the location.

        """
        self.locations = locations
        self.file_path = file_path

    def load(self):
        """
        Load the location data from the XML file.

        This method parses the XML file specified by `file_path` and extracts the location information.
        It populates the `tree` and `root` attributes with the parsed XML data.
        It also initializes other attributes such as `locationLen`, `location_id`, `location_name`, `location_description`, `items`, `moves`, `item_ids`, and `destination_location_ids` based on the parsed data.

        Returns:
            None
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
                        'destination_location_id')] = Move(self.move.get('move_id'), self.move.find('name').text, self.move.find('description').text, self.move.get('destination_location_id'))

            self.newLocation = Location(
                id=self.location_id, name=self.location_name, description=self.location_description, items=self.item_ids, possible_moves=self.destination_location_ids)
            self.locations[self.location_id] = self.newLocation

    def locations(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        return self.locations
