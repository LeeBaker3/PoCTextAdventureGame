from item import Item


class ItemList(list):

    def append(self, item: Item) -> None:
        if super().__len__() < self.maxListLength:
            return super().append(item)
        else:
            raise Exception(
                "Can't have more than {} itmes".format(self.maxListLength))

    @property
    def maxListLength(self):
        return self.__maxListLength

    @maxListLength.setter
    def maxListLength(self, value):
        self.__maxListLength = value
