from typing import Protocol, Dict
from btree.node import Node, NodeState # type: ignore
import zenoh # type: ignore
import json
import time
import logging

logging.getLogger().setLevel(logging.DEBUG)

class Node_class(Protocol):
    def Evaluate(self):
        pass

def get_status(key_expression: str) -> Dict[str, str]:
    """
    Get status of the node from hardware modules through zenoh.
    """
    session = zenoh.open(zenoh.Config())
    replies = session.get(key_expression, zenoh.Queue(), zenoh.QueryTarget.ALL())
    for reply in replies:
        try:
            value = json.loads(reply.ok.payload.decode("utf-8"))
        except:
            value = json.loads(reply.err.payload.decode("utf-8"))
        return value
    session.close()
    return {}

class Intake_new_sample(Node):
    def Evaluate(self):
        logging.warning("Intake_new_Sample")
        state = NodeState.SUCCESS
        return state
    
class Sample_quality_check(Node):
    def Evaluate(self):
        logging.warning("Sample_quality_check")
        state = NodeState.SUCCESS
        return state
    
class Sample_purification(Node):
    def Evaluate(self):
        logging.warning("Sample_purification")
        state = NodeState.SUCCESS
        return state

class Sample_processing(Node):
    def Evaluate(self):
        logging.warning("Sample_processing")
        state = NodeState.SUCCESS
        return state

class Detection(Node):
    def Evaluate(self):
        logging.warning("Detection")
        state = NodeState.SUCCESS
        return state
    
class Result_and_cleanup(Node):
    def Evaluate(self):
        logging.warning("Result_and_cleanup")
        state = NodeState.SUCCESS
        return state

class TipAvailable(Node):
    def Evaluate(self):
        keyexpression = "TipRm/trigger?timestamp={}&event=tip_available".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("TipAvailable: {}".format(state))
        return state

class TipAvailableInTray(Node):
    def Evaluate(self):
        logging.warning("TipAvailableInTray")
        keyexpression = "TipRm/trigger?timestamp={}&event=tip_available_in_tray".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("TipAvailableInTray: {}".format(state))
        return state

class MoveTipSliderToPos(Node):
    def Evaluate(self):
        logging.warning("MoveTipSliderToPos")
        keyexpression = "TipRm/trigger?timestamp={}&event=move_tip_slider_to_pos".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("MoveTipSliderToPos: {}".format(state))
        return state

class PickUp(Node):
    def Evaluate(self):
        logging.warning("PickUp")
        keyexpression = "Orchestrator/trigger?timestamp={}&event=pick_up".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("PickUp: {}".format(state))
        return state

class CaughtTipFirmAndOriented(Node):
    def Evaluate(self):
        logging.warning("CaughtTipFirmAndOriented")
        keyexpression = "TipChecker/trigger?timestamp={}&event=caught_tip_firm_and_orient".format(time.time())
        _keyexpression = "Orchestrator/trigger?timestamp={}&event=caught_tip_firm_and_oriented".format(time.time())
        result = get_status(keyexpression)
        _result = get_status(_keyexpression)
        print(result)
        if result != {} and _result != {}:
            if result["response_type"] == "Accepted" and _result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("CaughtTipFirmAndOriented: {}".format(state))
        return state

class PickupSuccess(Node):
    def Evaluate(self):
        logging.warning("PickupSuccess")
        keyexpression = "TipRm/trigger?timestamp={}&event=pick_up_success".format(time.time())
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("PickupSuccess: {}".format(state))
        return state

class DiscardCurrentTray(Node):
    def Evaluate(self):
        logging.warning("DiscardCurrentTray")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=discard_current_tray"
        result = get_status(keyexpression)
        print("class: {}".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("DiscardCurrentTray: {}".format(state))
        return state

class DiscardSuccess(Node):
    def Evaluate(self):
        logging.warning("DiscardSuccess")
        keyexpression = "Pipette/trigger?timestamp=123456789&event=discard_success"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("DiscardSuccess: {}".format(state))
        return state

class TrayAvailable(Node):
    def Evaluate(self):
        logging.warning("TrayAvailable")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=tray_available"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("TrayAvailable: {}".format(state))
        return state

class SliderMoveToLoad(Node):
    def Evaluate(self):
        logging.warning("SliderMoveToLoad")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=slider_move_to_load"
        result = get_status(keyexpression)
        print("class: {}".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("SliderMoveToLoad: {}".format(state))
        return state

class LoadNextTray(Node):
    def Evaluate(self):
        logging.warning("LoadNextTray")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=load_next_tray"
        result = get_status(keyexpression)
        logging.warning("LoadNextTray result: {} in class".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("LoadNextTray: {}".format(state))
        return state

class LoadSuccess(Node):
    def Evaluate(self):
        logging.warning("LoadSuccess")
        keyexpression = "Pipette/trigger?timestamp=123456789&event=load_success"
        result = get_status(keyexpression)
        logging.warning("LoadSuccess result: {} in class".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("LoadSuccess: {}".format(state))
        return state
    
class AlreadyInPos(Node):
    def Evaluate(self):
        logging.warning("AlreadyInPos")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=already_in_pos"
        result = get_status(keyexpression)
        logging.warning("MoveTipSlider result: {} in class".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("AlreadyInPos: {}".format(state))
        return state
    
class MoveTipSlider(Node):
    def Evaluate(self):
        logging.warning("MoveTipSlider")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=move_tip_slider"
        result = get_status(keyexpression)
        logging.warning("MoveTipSlider result: {} in class".format(result))
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("MoveTipSlider: {}".format(state))
        return state
    
class SliderReached(Node):
    def Evaluate(self):
        logging.warning("SliderReached")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=slider_reached"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("SliderReached: {}".format(state))
        return state

class GoToDiscardPos(Node):
    def Evaluate(self):
        logging.warning("GoToDiscardPos")
        keyexpression = "Orchestrator/trigger?timestamp=123456789&event=goto_discard_position"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("GoToDiscardPos: {}".format(state))
        return state
    
class PrepareToDiscard(Node):
    def Evaluate(self):
        logging.warning("PrepareToDiscard")
        keyexpression = "TipRm/trigger?timestamp=123456789&event=prepare_to_discard"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("PrepareToDiscard: {}".format(state))
        return state
    
class EjectTip(Node):
    def Evaluate(self):
        logging.warning("EjectTip")
        keyexpression = "Pipette/trigger?timestamp=123456789&event=eject_tip"
        result = get_status(keyexpression)
        print(result)
        if result != {}:
            if result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("EjectTip: {}".format(state))
        return state

class RetryCountBelowThreshold(Node):
    def Evaluate(self):
        logging.warning("RetryCountBelowThreshold")
        return NodeState.FAILURE
    
class DiscardTipSuccess(Node):
    def Evaluate(self):
        logging.warning("DiscardTipSuccess")
        keyexpression = "Pipette/trigger?timestamp=123456789&event=discard_tip_success"
        _keyexpression = "TipChecker/trigger?timestamp=123456789&event=discard_tip_success"
        result = get_status(keyexpression)
        _result = get_status(_keyexpression)
        print(result)
        if result != {} and _result != {}:
            if result["response_type"] == "Accepted" and _result["response_type"] == "Accepted":
                state = NodeState.SUCCESS
            else:
                state = NodeState.FAILURE
        else:
            state = NodeState.FAILURE
        logging.warning("DiscardTipSuccess: {}".format(state))
        return state