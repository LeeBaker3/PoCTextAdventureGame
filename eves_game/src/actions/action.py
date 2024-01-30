from abc import ABC, abstractclassmethod


class Action(ABC):

    @abstractclassmethod
    def action(self) -> (bool, str):
        pass

    @property
    def action_type(self) -> str:
        return self._action_type

    @action_type.setter
    def action_type(self, value: str) -> None:
        if value in self.actions:
            self._action_type = value
        else:
            raise ValueError(f"This isn't a support action type {value}.")

    @property
    def actions(cls) -> list[str]:
        return ['player', 'location', 'move_location']
