class Rule:

    def __init__(self, name, state1, state2, signal, action):
        self.name = name
        self.triggering_state = state1
        self.new_state = state2
        self.signal = signal
        self.action = action

    def do_action(self, agent, signal):
        pass

    def __str__(self):
        return self.name + ", triggering state: " + str(self.triggering_state) + \
               ", new state: " + str(self.new_state) + \
               ", signal: " + str(self.signal) + \
               ", action: " + str(self.action)


class Fsm:
    """ FSM class. """
    rules = []

    def __init__(self):
        self.current_rule = None

    def read_state(self):
        """ Returns the current state of the FSM. """
        return self.current_rule.name

