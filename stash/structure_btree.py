#type: ignore
import py_trees

def get_tip():
    #create all behaviours
    get_tip = py_trees.composites.Sequence("get_tip", memory=None)
    tip_available = py_trees.behaviours.Success("tip_available")
    prepare_tip_for_pickup = py_trees.composites.Selector("prepare_tip_for_pickup", memory=None)
    pick_up_using_orchestrator = py_trees.composites.Sequence("pick_up_using_orchestrator", memory=None)
    pick_up_success = py_trees.behaviours.Success("pick_up_success")

    #prepare_tip_for_pickup
    tip_available_in_tray = py_trees.composites.Sequence("tip_available_in_tray", memory=None)
    move_tip_slider_to_pos = py_trees.composites.Selector("move_tip_slider_to_pos", memory=None)

    #pick_up_using_orchestrator
    pick_up = py_trees.composites.Selector("pick_up", memory=None)
    caught_tip_firm_and_orient = py_trees.composites.Selector("caught_tip_firm_and_orient", memory=None)

    #tip_available_in_tray
    discard_current_tray = py_trees.composites.Selector("discard_current_tray", memory=None)
    current_tray_present = py_trees.composites.Selector("current_tray_present", memory=None)
    slider_move_to_discard = py_trees.behaviours.Success("slider_move_to_discard")
    discard_pickup_current_tray = py_trees.behaviours.Success("discard_pickup_current_tray")
    dicard_success = py_trees.behaviours.Success("dicard_success")

    #load_new_tray
    tray_available = py_trees.composites.Selector("tray_available", memory=None)
    slider_move_to_load = py_trees.behaviours.Success("slider_move_to_load")
    load_new_tray = py_trees.composites.Selector("load_next_tray", memory=None)
    load_success = py_trees.behaviours.Success("load_success")

    #move_tip_slider_to_pos
    already_in_pos = py_trees.composites.Selector("already_in_pos", memory=None)
    move_tip_slider = py_trees.behaviours.Success("move_tip_slider")
    slider_reached = py_trees.behaviours.Success("slider_reached")

    #pick_up_using_orchestrator
    pick_up = py_trees.behaviours.Success("pick_up")
    caught_tip_firm_and_orient = py_trees.composites.Selector("caught_tip_firm_and_orient", memory=None)

    #caught_tip_firm_and_orient
    discard_tip = py_trees.composites.Selector("dicard_tip", memory=None)

    #discard_tip
    go_to_discard_position = py_trees.behaviours.Success("go_to_discard_position")
    prepare_to_discard = py_trees.behaviours.Success("prepare_to_discard")
    eject_tip = py_trees.behaviours.Success("eject_tip")
    discard_tip_success = py_trees.composites.Sequence("discard_tip_success", memory=None)
    retry_count_below_threshold = py_trees.composites.Sequence("retry_count_below_threshold", memory=None)

    #compose tree
    discard_tip_success.add_children([retry_count_below_threshold])
    discard_tip.add_children([go_to_discard_position, prepare_to_discard, eject_tip, discard_tip_success])
    
    discard_current_tray.add_children([current_tray_present, slider_move_to_discard, discard_pickup_current_tray, dicard_success])
    load_new_tray.add_children([tray_available, slider_move_to_load, load_success])
    move_tip_slider_to_pos.add_children([already_in_pos, move_tip_slider, slider_reached])
    caught_tip_firm_and_orient.add_children([discard_tip])

    tip_available_in_tray.add_children([discard_current_tray, load_new_tray])

    pick_up_using_orchestrator.add_children([pick_up, caught_tip_firm_and_orient])

    get_tip.add_children([tip_available, prepare_tip_for_pickup, pick_up_using_orchestrator, pick_up_success])

    return get_tip

if __name__ == '__main__':
    root = get_tip()
    root.setup(timeout=15)
    for i in range(0, 5):
        root.tick_once()
        print(root.status)
    
