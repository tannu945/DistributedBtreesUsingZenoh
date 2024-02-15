from btree.node import Node, NodeState # type: ignore
import logging

logging.getLogger().setLevel(logging.DEBUG)

class Selector(Node):
    """
    Evaluate the children which needs hardware validation.
    """
    def __init__(self, children) -> None:
        super().__init__(children)
    
    def Evaluate(self) -> NodeState:
        for child in self.children:
            childStatus = child.Evaluate()
            logging.info("Child status: {} of child  {}".format(childStatus, child))
            if childStatus == NodeState.FAILURE:
                continue
            elif childStatus == NodeState.SUCCESS:
                state = NodeState.SUCCESS
                logging.debug("Returning state from selector: {}".format(state))
                return state
            elif childStatus == NodeState.RUNNING:
                state = NodeState.RUNNING
                logging.debug("Returning state from selector: {}".format(state))
                return state
            else:
                continue
        state = NodeState.FAILURE
        logging.debug("Returning state from selector: {}".format(state))
        return state