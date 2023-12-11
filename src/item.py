import xml.etree.ElementTree as ET


class Item:
    """_summary_
    """

    def __init__(self, id: str, name: str, description: str):
        self.item_id = id
        self.item_name = name
        self.item_description = description


class LoadItems:
    """_summary_
    """

    def __init__(self, items, file_path):
        self.items = items
        self.file_path = file_path

    def load(self):
        """_summary_
        """

        self.tree = ET.parse(self.file_path)
        self.root = self.tree.getroot()

        self.item_len = len(self.root.findall("item"))

        for self.child in self.root:
            self.item_id = self.child.get('item_id')
            self.item_name = self.child.find('item_name').text
            self.item_description = self.child.find(
                'item_description').text

            self.newItem = Item(
                self.item_id, self.item_name, self.item_description)
            self.items[self.item_id] = self.newItem

    def items(self):
        return self.items
