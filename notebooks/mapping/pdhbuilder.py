from abc import ABC, abstractmethod
from typing import Any


class Builder(ABC):
    """Specifies methods for creating node objects."""

    @property
    @abstractmethod
    def node(self) -> None:
        pass

    @abstractmethod
    def produce_element(self, element) -> None:
        pass

    @abstractmethod
    def produce_attribute(self, attribute) -> None:
        pass


class ValueBuilder(Builder):
    """Creates a ValueBuilder object."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._node = ValueNode()

    @property
    def node(self): # -> ValueNode:
        node = self._node
        self.reset()
        return node

    def produce_element(self, element) -> None:
        self._node.add(element)

    def produce_attribute(self, attribute) -> None:
        self._node.add(attribute)


class ValueNode():
    """A ValueNode represents the PDH value element."""

    def __init__(self) -> None:
        self.nodes = []

    def add(self, node: Any) -> None:
        self.nodes.append(node)

    def list_nodes(self) -> None:
        print(f"Nodes in this element: {', '.join(self.nodes)}", end ="")


if __name__ == "__main__":
    builder = ValueBuilder()
    builder.produce_attribute("key")
    builder.produce_element("Test")
    builder.node.list_nodes()
