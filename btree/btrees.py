from btree import tree, selector, sequence #type: ignore
from btree import btree_classes

class Workflow_btree(tree.Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            selector.Selector([btree_classes.Intake_new_sample()]),
            selector.Selector([btree_classes.Sample_quality_check()]),
            sequence.Sequence([
                    selector.Selector([btree_classes.TipAvailable()]),
                    sequence.Sequence([
                        selector.Selector([btree_classes.TipAvailableInTray(),
                            sequence.Sequence([
                                btree_classes.DiscardCurrentTray(),
                                selector.Selector([btree_classes.DiscardSuccess()]),
                                sequence.Sequence([
                                    selector.Selector([btree_classes.TrayAvailable()]),
                                    btree_classes.SliderMoveToLoad(),
                                    btree_classes.LoadNextTray()
                                ]),
                                selector.Selector([btree_classes.LoadSuccess()]),
                                ])
                        ]),
                        selector.Selector([btree_classes.MoveTipSliderToPos(),
                            sequence.Sequence([
                                selector.Selector([btree_classes.AlreadyInPos()]),
                                btree_classes.MoveTipSlider(),
                                selector.Selector([btree_classes.SliderReached()])
                                ])
                            ])
                    ]),
                    sequence.Sequence([
                        btree_classes.PickUp(),
                        selector.Selector([btree_classes.CaughtTipFirmAndOriented(),
                            selector.Selector([
                                sequence.Sequence([
                                    btree_classes.GoToDiscardPos(),
                                    btree_classes.PrepareToDiscard(),
                                    btree_classes.EjectTip(),
                                    selector.Selector([btree_classes.DiscardTipSuccess(),
                                        selector.Selector([btree_classes.RetryCountBelowThreshold()])
                                    ])
                                ])
                            ])
                        ])
                    ]),
                    selector.Selector([btree_classes.PickupSuccess()])
                ]),
            selector.Selector([btree_classes.Sample_processing()]),
            selector.Selector([btree_classes.Sample_processing()]),
            selector.Selector([btree_classes.Detection()]),
            selector.Selector([btree_classes.Result_and_cleanup()]),
        ])
        return root

class Tip_Available_In_Tray(tree.Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            btree_classes.DiscardCurrentTray(),
            selector.Selector([btree_classes.DiscardSuccess()]),
            sequence.Sequence([
                selector.Selector([btree_classes.TrayAvailable()]),
                btree_classes.SliderMoveToLoad(),
                btree_classes.LoadNextTray()
            ]),
            selector.Selector([btree_classes.LoadSuccess()]),
        ])
        return root

class Move_tip_slider_to_pos(tree.Tree):
    def SetUpTree(self):
        root = sequence.Sequence([
            selector.Selector([btree_classes.AlreadyInPos()]),
            btree_classes.MoveTipSlider(),
            selector.Selector([btree_classes.SliderReached()])
        ])
        return root

class Discard_tip_success(tree.Tree):
    def SetUpTree(self):
        root = selector.Selector([btree_classes.RetryCountBelowThreshold()])
        return root

class Caught_tip_firm_and_orient(tree.Tree):
    def SetUpTree(self):
        root = selector.Selector([
            sequence.Sequence([
                btree_classes.GoToDiscardPos(),
                btree_classes.PrepareToDiscard(),
                btree_classes.EjectTip(),
                selector.Selector([btree_classes.DiscardTipSuccess()])
            ])
        ])
        return root