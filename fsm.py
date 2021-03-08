import re
from typing import Callable
from kpc_agent import kpc_instance as kpc


class Rule:
    """Rule class"""

    def __init__(self, target_state: str, signal: str, action: Callable, action_takes_parameter: bool):
        self.target_state = target_state
        self.signal = signal
        self.action = action
        self.action_takes_parameter = action_takes_parameter

    def is_me(self, input):
        return not re.match(self.signal, input) is None


WAKEUP_RULE = Rule("read", ".", kpc.wakeup, False)
DIGIT_RULE = Rule("read", r"\d", kpc.fsm_signal, True)
END_PASS_RULE = Rule("verify", r"\*", kpc.verify_login, False)
CORRECT_PASS_RULE = Rule("active", "Y", kpc.reset_buffer, False)
WRONG_PASS_RULE = Rule("read", "N", kpc.reset_buffer, False)
SET_NEW_PASS_RULE = Rule("read2", r"\*", None, False)
CHOOSE_LED_RULE = Rule("led", r"\d", kpc.fsm_signal, True)
CHOOSE_DURATION_RULE = Rule("active", r"\d", kpc.light_led, True)
ABORT_NEW_PASS_RULE = Rule("active", "#", kpc.reset_buffer, False)
ENTER_NEW_PASS_1_RULE = Rule("read2", r"\d", kpc.fsm_signal, True)
END_NEW_PASS_1_RULE = Rule("read3", r"\*", kpc.fsm_signal, True)
ENTER_NEW_PASS_2_RULE = Rule("read3", r"\d", kpc.fsm_signal, True)
END_NEW_PASS_2_RULE = Rule(
    "active", r"\*", kpc.validate_passcode_change, False)
LOGOUT_RULE = Rule("init", "#", kpc.power_down, False)


class Fsm:
    """ FSM class. """
    states = {
        "init":   [WAKEUP_RULE],
        "read":   [DIGIT_RULE, END_PASS_RULE],
        "verify": [CORRECT_PASS_RULE, WRONG_PASS_RULE],
        "active": [SET_NEW_PASS_RULE, LOGOUT_RULE, CHOOSE_LED_RULE],
        "led":    [CHOOSE_DURATION_RULE],
        "read2":  [ENTER_NEW_PASS_1_RULE, ABORT_NEW_PASS_RULE, END_NEW_PASS_1_RULE],
        "read3":  [ENTER_NEW_PASS_2_RULE, ABORT_NEW_PASS_RULE, END_NEW_PASS_2_RULE]
    }

    def __init__(self):
        self.current_state = "init"

    def next_action(self):
        signal = kpc.get_next_signal()
        print(signal)
        print(self.current_state)

        for action in Fsm.states[self.current_state]:
            if action.is_me(signal):
                if action.action:
                    if action.action_takes_parameter:
                        action.action(signal)
                    else:
                        action.action()
                self.current_state = action.target_state
        self.next_action()


FSM = Fsm()
FSM.next_action()
