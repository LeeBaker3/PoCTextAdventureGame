from item import Item


class ItemList(list):

    def append(self, item: Item) -> None:
        if super().__len__() < self.max_list_length:
            return super().append(item)
        else:
            raise Exception(
                "Can't have more than {} items".format(self.max_list_length))

    @property
    def max_list_length(self):
        return self.__max_list_length

    @max_list_length.setter
    def max_list_length(self, value):
        self.__max_list_length = value

    def items_in_list(self) -> str:
        self.items = ''
        for self.item in self:
            self.items = '- ' + self.item.item_name + '\n' + self.items
        return self.items
