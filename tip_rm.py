from typing import Protocol, Iterator
from contextlib import contextmanager
from btree import btrees, node
import logging
import time
import zenoh # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

class TipRM(Protocol):
    def tip_available(self) -> str:
        ...

    def tip_available_in_tray(self) -> str:
        ...

    def discard_current_tray(self) -> str:
        ...

    def tray_available(self) -> str:
        ...

    def slider_move_to_load(self) -> str:
        ...

    def load_next_tray(self) -> str:
        ...
    
    def prepare_to_discard(self) -> str:
        ...

    def move_tip_slider(self) -> str:
        ...
    
    def pickup_success(self) -> str:
        ...
    
    def move_tip_slider_to_pos(self) -> str:
        ...
    
    def slider_reached(self) -> str:
        ...
    
    def already_in_pos(self) -> str:
        ...

class Tip_rm:
    def tip_available(self) -> str:
        #logging.debug("Checking if tip is available.")
        '''
        if node.Node.getData("Tipcount") > 0:
            return "Accepted"
        else:
            return "No tips available."'''
        return "Accepted"

    def tip_available_in_tray(self) -> str:
        #logging.debug("Checking if tip is available in tray.")
        #tipcount = node.Node.getData(key="TipTraycount")
        #if tipcount > 0:
        '''tipavailableintray = btrees.Tip_Available_In_Tray()
        root = tipavailableintray.SetUpTree()
        result = root.Evaluate()
        if result == node.NodeState.SUCCESS:
            return "Accepted"
        else:
            return "No tips available in tray."
        #else:
        #    return "No tips available in tray."'''
        return "Accepted"

    def discard_current_tray(self) -> str:
        #logging.debug("Discarding current tray.")
        return "Accepted"

    def tray_available(self) -> str:
        #logging.debug("Checking if tray is available.")
        '''
        if node.Node.getData("Traycount") > 0:
            return "Accepted"
        else:
            return "No trays available."'''
        return "Accepted"

    def slider_move_to_load(self) -> str:
        #logging.debug("Slider moving to load.")
        return "Accepted"

    def load_next_tray(self) -> str:
        #logging.debug("Loading next tray.")
        return "Accepted"
    
    def prepare_to_discard(self) -> str:
        #logging.debug("Preparing to discard.")
        return "Accepted"

    def move_tip_slider_to_pos(self) -> str:
        #logging.debug("Moving tip slider to position.")
        movetipslidertopos = btrees.Move_tip_slider_to_pos()
        root = movetipslidertopos.SetUpTree()
        result = root.Evaluate()
        if result == "Accepted":
            return "Accepted"
        else:
            #logging.debug("Problem in moving tip slider to position.")
            return "Problem in moving tip slider to position."
    
    def pickup_success(self) -> str:
        #logging.debug("Pickup success.")
        return "Accepted"
    
    def move_tip_slider(self) -> str:
        #logging.debug("Moving tip slider.")
        return "Accepted"
    
    def slider_reached(self) -> str:
        #logging.debug("Slider reached.")
        return "Accepted"
    
    def already_in_pos(self) -> str:
        #logging.debug("Already in position.")
        return "Accepted"

class Queryable:
    def __init__(self, Tip_rm: TipRM) -> None:
        self.Tip_rm = Tip_rm
        
    def check_status(self, node: TipRM, event: str) -> str:
        return node.__getattribute__(event)()

    def trigger_queryable_handler(self, query: zenoh.Query) -> None:
        try:
            #logging.debug("Received query: {}".format(query.selector))
            event = query.selector.decode_parameters()
            result = self.check_status(self.Tip_rm, event['event'])
            #print(result + " " + event['event'])
            if result == "Accepted":
                payload = {"response_type":"Accepted","response":result}
            else:
                payload = {"response_type":"Rejected","response":result}
        except ValueError as e:
            payload = {"response_type":"Rejected","response":"{}".format(e)}

        logging.debug("Sending response for event {}".format(event['event']))
        query.reply(zenoh.Sample("TipRm/trigger", payload))

class Session:
    def __init__(self, handler: Queryable) -> None:
        self.handler = handler
    def open(self):
        self.config = zenoh.Config()
        self.session = zenoh.open(self.config)
        self.trigger_queryable = self.session.declare_queryable("TipRm/trigger", self.handler.trigger_queryable_handler)
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
    tip_rm = Tip_rm()
    handler = Queryable(tip_rm)
    with session_manager(handler) as session:
        logging.debug("Tip RM Started...")
        while True:
            time.sleep(1)