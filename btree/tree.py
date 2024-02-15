from btree.node import Node # type: ignore

class Tree:
    _root: Node = None # type: ignore

    def Start(self):
        Tree._root = self.SetupTree()
    
    def Update(self):
        if Tree._root!=None:
            Tree._root.Evaluate()
    
    def SetupTree(self):
        ...    