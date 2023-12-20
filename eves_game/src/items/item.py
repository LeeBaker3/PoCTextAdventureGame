import xml.etree.ElementTree as ET


class Item:
    """_summary_
    """

    def __init__(self, id: str, name: str, description: str, actions: dict = None):
        self.item_id = id
        self.item_name = name
        self.item_description = description
        self.actions = actions


class LoadItems:
    """_summary_
    """

    def __init__(self, items: dict, file_path: str):
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
            self.item_actions = self.child.find('item_actions')

            self.item_actions_extracted = {}
            self.actions_len = len(self.item_actions.findall("action"))
            if self.item_actions is not None:
                for self.action in self.item_actions:
                    self.item_actions_extracted[self.action.find(
                        'action_name').text] = {'action_description': self.action.find('action_description').text, 'holding': self.action.get('holding')}

            self.newItem = Item(
                self.item_id, self.item_name, self.item_description, self.item_actions_extracted)
            self.items[self.item_id] = self.newItem

    def items(self):
        return self.items
