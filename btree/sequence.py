from btree.node import Node, NodeState # type: ignore
import logging

logging.getLogger().setLevel(logging.DEBUG)

class Sequence(Node):
    """
    Evaluate the children which doesn't need hardware validation.
    """
    def __init__(self, children) -> None:
        super().__init__(children)

    def Evaluate(self) -> NodeState:
        anychildisrunning = False
        for child in self.children:
            childStatus = child.Evaluate()
            logging.info("Child status: {} of child  {}".format(childStatus, child))
            if childStatus == NodeState.FAILURE:
                state = NodeState.FAILURE
                logging.debug("Returning state from sequence: {}".format(state))
                return state
            elif childStatus == NodeState.SUCCESS:
                continue
            elif childStatus == NodeState.RUNNING:
                anychildisrunning = True
                continue
            else:
                state = NodeState.SUCCESS
                logging.debug("Returning state from sequence: {}".format(state))
                return state
            
        state = NodeState.RUNNING if anychildisrunning else NodeState.SUCCESS
        logging.debug("Returning state from sequence: {}".format(state))
        return state