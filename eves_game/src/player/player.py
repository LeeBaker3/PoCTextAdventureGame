from src.item_list import ItemList
from src.items.item import Item


class Player():
    """_summary_
    """

    def __init__(self, player_name: str, max_item_length: int = 3):
        """_summary_

        Args:
            player_name (str): _description_
            max_item_length (int, optional): _description_. Defaults to 3.
        """
        self._player_name = player_name
        self._player_items = ItemList()
        self.max_item_length = max_item_length

    @ property
    def player_name(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._player_name

    @ property
    def max_item_length(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._player_items.max_list_length

    @ max_item_length.setter
    def max_item_length(self, value: int):
        """_summary_

        Args:
            value (_type_): _description_
        """
        self._player_items.max_list_length = value

    def add_item(self, item: Item) -> bool:
        """_summary_

        Args:
            item (_type_): _description_

        Returns:
            bool: _description_
        """
        try:
            self._player_items.append(item)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return False
            # Add messaging
        return True

    def remove_item(self, item: Item) -> bool:
        """_summary_

        Args:
            item (_type_): _description_

        Returns:
            bool: _description_
        """
        self._player_items.remove(item)

    @property
    def player_items_length(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return len(self._player_items)

    def player_items(self) -> ItemList:
        return self._player_items
