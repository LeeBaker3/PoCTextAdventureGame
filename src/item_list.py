from src.items.item import Item


class ItemList(list):

    def append(self, item: Item) -> None:
        """_summary_

        Args:
            item (Item): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        if super().__len__() < self.max_list_length:
            return super().append(item)
        else:
            raise Exception(
                "Can't have more than {} items".format(self.max_list_length))

    @ property
    def max_list_length(self):
        """_summary_

        Returns:
            None:
        """
        return self.__max_list_length

    @ max_list_length.setter
    def max_list_length(self, value: int):
        """_summary_
        Method set/update the integer value for max number of items in
        the ItemList

        Args:
            value (int): 
        """
        self.__max_list_length = value

    def items_in_list(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        self.items = ''
        for self.item in self:
            self.items = '- ' + self.item.item_name + '\n' + self.items
        return self.items
