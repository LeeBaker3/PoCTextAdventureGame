from inspect import getmembers, isclass, isabstract
import src.actions as actions


class ActionFactory(object):
    action_implementations = {}

    def __init__(self) -> None:
        self.load_actions_types()

    def load_actions_types(self) -> None:
        implementations = getmembers(
            actions, lambda a: isclass(a) and not isabstract(a))
        for name, _type in implementations:
            if isclass(_type) and issubclass(_type, actions.Action):
                self.action_implementations[name] = _type

    def create(self, action_type: str, player: 'Player', location: 'Location', item: 'Item') -> object:
        if action_type in self.action_implementations:
            return self.action_implementations[action_type](player, location, item)
        else:
            raise ValueError(f'{action_type} is not currently implemented')
