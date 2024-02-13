from typing import Iterator, Dict
from contextlib import contextmanager
from btree.btrees import Workflow_btree
from btree.node import NodeState
import logging
import time
import zenoh # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class Queryable:
    def __init__(self, btree) -> None:
        self.btree = btree

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            logging.debug("Received query: {}".format(query.selector))
            root = self.btree.SetUpTree()
            result = root.Evaluate()
            if result != None:
                if result == NodeState.SUCCESS:
                    payload = {"response_type":"Accepted","response":"Module is responding."}
                else:
                    payload = {"response_type":"Rejected","response":"Module is not responding. Please check Connection."}
            else:
                payload = {"response_type":"Rejected","response":"Module is not responding. Please check Connection."}
        except ValueError as e:
            payload = {"response_type":"Rejected", "response": "{}".format(e)}
        query.reply(zenoh.Sample("Workflow/trigger", payload))

class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    
    def open(self):
        global keyexpression
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("Workflow/trigger", self.handler.trigger_queryable_handler)
        
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
    btree = Workflow_btree()
    handler = Queryable(btree)
    with session_manager(handler) as session:
        logging.debug("Workflow Started...")
        while True:
            time.sleep(1)