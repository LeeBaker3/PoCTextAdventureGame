from src.item_list import ItemList


class Player():

    def __init__(self, player_name: str, max_item_length: int = 3):
        self._player_name = player_name
        self._player_items = ItemList()
        self.max_item_length = max_item_length

    @ property
    def player_name(self):
        return self._player_name

    @ property
    def max_item_length(self):
        return self._player_items.max_list_length

    @ max_item_length.setter
    def max_item_length(self, value):
        self._player_items.max_list_length = value

    def add_item(self, item) -> bool:
        try:
            self._player_items.append(item)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return False
            # Add messaging
        return True

    def remove_item(self, item) -> bool:
        self._player_items.remove(item)
