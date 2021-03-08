class Fsm:
    """ FSM class. """
    states = {0: "Init",
              1: "Read1",
              2: "verify",
              3: "Active",
              4: "Read2",
              5: "Read3"}

    def __init__(self):
        self.state = 0

    def set_state(self, new_state):
        """ If valid changes the state of FSM. """
        if new_state in self.states.keys():
            self.state = new_state
        else:
            raise ValueError("Invalid state")

    def read_state(self):
        """ Returns the current state of the FSM. """
        return self.states[self.state] + ", Statenr: " + str(self.state)

    def fsm_loop(self):
        """ Main FSM-loop. """
        while True:
            if self.state == 0:  # and input == something:
                self.set_state(1)
            if self.state == 1:  # and input == *:
                self.set_state(2)
            if self.state == 2:
                if correct_password:
                    self.set_state(3)
                else:
                    self.set_state(0)
            if self.state == 3:  # and input == *:
                self.set_state(4)
            if self.state == 4:  # and input == *:
                self.set_state(5)
            if self.state == 5:
                self.set_state(3)


def main():
    fsm = Fsm()
    fsm.set_state(5)
    print(fsm.read_state())


if __name__ == '__main__':
    main()
