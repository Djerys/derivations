from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def is_nonterminal(self):
        pass


class NonTerminalNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self._children = []

    def __repr__(self):
        return '{}({})'.format(
            self.name,
            ''.join(str(c) for c in self._children)
        )

    def is_nonterminal(self):
        return True

    def add(self, children):
        if not self._children:
            self._children = children
            return True

        for child in self._children:
            if child.is_nonterminal():
                was_changed = child.add(children)
                if was_changed:
                    return True


class LeafNode(Node):
    def is_nonterminal(self):
        return False

    def __repr__(self):
        return self.name
