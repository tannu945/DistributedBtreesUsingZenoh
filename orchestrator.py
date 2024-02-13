from typing import Protocol, Iterator
from contextlib import contextmanager
from btree import btrees
import logging
import time
import zenoh  # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class Orchestrator(Protocol):
    def pick_up(self) -> str:
        ...
    def caught_tip_firm_and_orient(self) -> str:
        ...
    def go_to_discard_position(self) -> str:
        ...
    def discard_tip_success(self) -> str:
        ...

class Orchestrator_:
    def pick_up(self) -> str:
        #logging.debug("Checking if tip is picked up.")
        return "Accepted"
    
    def caught_tip_firm_and_orient(self) -> str:
        #logging.debug("Checking if tip is caught, firm and oriented.")
        caughttipfirmandorient = btrees.Caught_tip_firm_and_orient()
        root = caughttipfirmandorient.SetUpTree()
        result = root.Evaluate()
        if result == "Accepted":
            return "Accepted"
        else:
            logging.debug("Orchestrator denied that tip does not caught firm and orient.")
            return "Orchestrator denied that tip does not caught firm and orient."

    def go_to_discard_position(self) -> str:
       # logging.debug("Going to discard position.")
        return "Accepted"
    
    def discard_tip_success(self) -> str:
        #logging.debug("Checking if tip is discarded successfully.")
        discardtipsuccess = btrees.Discard_tip_success()
        root = discardtipsuccess.SetUpTree()
        result = root.Evaluate()
        if result == "Accepted":
            return "Accepted"
        else:
            logging.debug("Orchestrator denied that tip does not discard successfully.")
            return "Orchestrator denied that tip does not discard successfully."

class Queryable:
    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator
        
    def check_status(self, node: Orchestrator, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            #logging.debug("Received query: {}".format(query.selector))
            event = query.selector.decode_parameters()
            result = self.check_status(self.orchestrator, event.event)
            if result == "Accepted":
                payload = {"response_type":"Accepted","response":"Successfully executed."}
            else:
                payload = {"response_type":"Rejected","response":result}
        except ValueError as e:
            payload = {"response_type":"Rejected", "response": "{}".format(e)}

        logging.debug("Sending response: {} for event {}".format(payload, event['event']))
        query.reply(zenoh.Sample("Orchestrator/trigger", payload))


class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("Orchestrator/trigger", self.handler.trigger_queryable_handler)
    def close(self):
        self.session.close()
        self.trigger_queryable.undeclare()    
    
@contextmanager
def session_manager(handler: Queryable) -> Iterator[Session]:
    try:
        session = Session(handler)
        session.open()
        yield session
    except KeyboardInterrupt:
        logging.error("Interrupted by user")
    finally:
        session.close()

if __name__ == "__main__":
    orchestrator = Orchestrator_()
    handler = Queryable(orchestrator)
    with session_manager(handler) as session:
        logging.debug("Orchestrator Started...")
        while True:
            time.sleep(1)