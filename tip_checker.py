from typing import Protocol, Iterator
from contextlib import contextmanager
from btree import btrees, node
import logging
import time
import zenoh # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class TipChecker(Protocol):
    def caught_tip_firm_and_orient(self) -> str:
        ... 
    def discard_tip_success(self) -> str:
        ...

class Tip_checker:
    def caught_tip_firm_and_orient(self) -> str:
        #logging.debug("Checking if tip is caught, firm and oriented.")
        caughttipfirmandorient = btrees.Caught_tip_firm_and_orient()
        root = caughttipfirmandorient.SetUpTree()
        result = root.Evaluate()
        if result == "Accepted":
            return "Accepted"
        else:
            logging.debug("TipChecker denied that tip does not caught firm and orient.")
            return "TipChecker denied that tip does not caught firm and orient."
        
    def discard_tip_success(self) -> str:
        #logging.debug("Checking if tip is discarded successfully.")
        discardtipsuccess = btrees.Discard_tip_success()
        root = discardtipsuccess.SetUpTree()
        result = root.Evaluate()
        if result == "Accepted":
            return "Accepted"
        else:
            logging.debug("TipChecker denied that tip does not discard successfully.")
            return "TipChecker denied that tip does not discard successfully."

class Queryable:
    def __init__(self, tip_checker: TipChecker) -> None:
        self.tip_checker = tip_checker
        
    def check_status(self, node: TipChecker, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            #logging.debug("Received query: {}".format(query.selector))
            event = query.selector.decode_parameters()
            result = self.check_status(self.tip_checker, event['event'])
            if result == "Accepted":
                payload = {"response_type":"Accepted","response":"Successfully executed."}
            else:
                payload = {"response_type":"Rejected","response":result}
        except ValueError as e:
            payload = {"response_type":"Rejected","response": "{}".format(e)}
        

        logging.debug("Sending response: {} for event {}".format(payload, event['event']))
        query.reply(zenoh.Sample("TipChecker/trigger", payload))


class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("TipChecker/trigger", self.handler.trigger_queryable_handler)
        
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
    tip_checker = Tip_checker()
    handler = Queryable(tip_checker)
    with session_manager(handler) as session:
        logging.debug("Tip Checker Started...")
        while True:
            time.sleep(1)