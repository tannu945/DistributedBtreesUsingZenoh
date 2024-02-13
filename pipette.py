from typing import Protocol, Iterator
from contextlib import contextmanager
from btree import btrees, node
import logging
import time
import zenoh # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class Pipette(Protocol):
    def discard_success(self) -> str:
        ...
    def load_success(self) -> str:
        ...
    def eject_tip(self) -> str:
        ...
    def discard_tip_success(self) -> str:
        ...

class Pipette_:
    def discard_success(self) -> str:
        #logging.debug("Checking if discard was successful.")
        return "Accepted"

    def load_success(self) -> str:
        #logging.debug("Checking if load was successful.")
        return "Accepted"

    def eject_tip(self) -> str:
        #logging.debug("Eject tip")
        return "Accepted"

    def discard_tip_success(self) -> str:
        #logging.debug("Checking if discard tip was successful.")
        discardtipsuccess = btrees.Discard_tip_success()
        root = discardtipsuccess.SetUpTree()
        result = root.Evaluate()
        if result == "Accepted":
            return "Accepted"
        else:
            logging.debug("Pipette denied that tip does not discard successfully.")
            return "Pipette denied that tip does not discard successfully."

class Queryable:
    def __init__(self, pipette: Pipette) -> None:
        self.pipette = pipette
        
    def check_status(self, node: Pipette, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            #logging.debug("Received query: {}".format(query.selector))
            event = query.selector.decode_parameters()
            result = self.check_status(self.pipette, event['event'])
            if result == "Accepted":
                payload = {"response_type":"Accepted","response":"Successfully executed."}
            else:
                payload = {"response_type":"Rejected","response":result}
        except ValueError as e:
            payload = {"response_type":"Rejected", "response": "{}".format(e)}

        logging.debug("Sending response for event {}".format(event['event']))
        query.reply(zenoh.Sample("Pipette/trigger", payload))

class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("Pipette/trigger", self.handler.trigger_queryable_handler)
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
    pipette = Pipette_()
    handler = Queryable(pipette)
    with session_manager(handler) as session:
        logging.debug("Pipette Started...")
        while True:
            time.sleep(1)