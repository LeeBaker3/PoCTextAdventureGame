from abc import ABC, abstractclassmethod


class Action(ABC):

    @abstractclassmethod
    def action(self) -> (bool, str):
        pass

    @property
    def action_group(self) -> str:
        return self._action_group

    @action_group.setter
    def action_group(self, value: str) -> None:
        if value in self.action_groups:
            self._action_group = value
        else:
            raise ValueError(f"This isn't a support action group {value}.")

    @property
    def action_groups(cls) -> list[str]:
        return ['Player', 'Location', 'MoveLocation']
