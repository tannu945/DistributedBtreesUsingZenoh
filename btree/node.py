from enum import Enum

class NodeState(Enum):
    """The state of a node."""
    RUNNING = 0
    SUCCESS = 1
    FAILURE = 2
    EXCEPTION =3
    ERROR = 4

class Node:
    "A node in behaviour tree."
    state: NodeState
    parent: object
    children: list = []
    _datacontext: dict[str, int] = {}

    def __init__(self, children=[]):
        # Initialize the node.
        Node.parent = None
        for child in children:
            self._Attach(child)

    def _Attach(self, node):
        # Attach a child node to this node.
        Node.parent = self
        self.children.append(node)

    def Evaluate(self) -> NodeState:
        # Evaluate the node. Overidden Function
        ...
    
    def setData(self, key: str, value: int) -> None:
        # Set the data in the datacontext.
        Node._datacontext[key] = value

    def getData(self, key: str) -> int:
        # Get the data from the datacontext.
        value = 0
        _value = Node._datacontext[key]
        if _value != 0:
            value = _value
            return value
        
        node = Node.parent
        while node != None:
            value = node.getData(key) #type: ignore
            if value != 0:
                return value
            node = node.parent #type: ignore
        return 0
    
    def clearData(self) -> None:
        # Clear the data in the datacontext.
        Node._datacontext.clear()