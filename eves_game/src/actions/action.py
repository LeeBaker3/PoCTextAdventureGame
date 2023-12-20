from abc import ABC, abstractclassmethod


class Action(ABC):

    @abstractclassmethod
    def action(self) -> (bool, str):
        pass
