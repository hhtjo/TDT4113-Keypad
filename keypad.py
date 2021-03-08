"""Module containing Keypad-parser"""
import time
from GPIOSimulator_v5 import GPIOSimulator, keypad_col_pins, keypad_row_pins

KEYPAD_BUTTONS = (
    ("1", "2", "3"),
    ("4", "5", "6"),
    ("7", "8", "9"),
    ("*", "0", "#")
)


class Keypad:
    """Class for interacting with Keypad"""

    def __init__(self) -> None:
        self.stream = ""
        self.gpio = GPIOSimulator()
        self.prev_btn = None
        self.setup()

    def setup(self):
        """Set up GPIO-pins for use with Keypad"""

        for row_pin in keypad_row_pins:
            #Set up row-pins
            self.gpio.setup(row_pin, self.gpio.OUT)

        for col_pin in keypad_col_pins:
            #Set up col-pins
            self.gpio.setup(col_pin, self.gpio.IN)

    def get_keypad_data(self):
        """Poll GPIO for button press"""
        active_col, active_row = None, None

        for row, row_pin in enumerate(keypad_row_pins):
            #Check Rows
            self.gpio.output(row_pin, self.gpio.HIGH)
            for col, col_pin in enumerate(keypad_col_pins):
                #Check Columns
                if self.gpio.input(col_pin) == self.gpio.HIGH:
                    active_col = col
                    active_row = row
            self.gpio.output(row_pin, self.gpio.LOW)
        return active_col, active_row

    def setup_poll(self):
        """Sets up poll and starts it"""
        while True:
            try:
                self.do_polling()
                time.sleep(0.01)
            except KeyboardInterrupt:
                print(self.get_stream())
                exit()

    def do_polling(self):
        """Polls the keypad"""
        keypad_press = self.get_keypad_data()
        current_button = Keypad.parse_result(keypad_press[0], keypad_press[1])

        if current_button != self.prev_btn:
            #Changed button
            if not self.prev_btn is None:
                self.stream += self.prev_btn
            self.prev_btn = current_button

    def get_next_signal(self):
        """Get a signal from keypad"""
        keypress = None

        while not keypress:
            #While no keypress received
            self.do_polling()
            if self.stream:
                keypress = self.get_stream()[0]
            time.sleep(0.01)

        return keypress

    def get_stream(self):
        """Returns and clears stream"""
        result = self.stream
        self.stream = ""
        return result

    @staticmethod
    def parse_result(col: int, row: int):
        """Parses active col and row to keypad input """
        try:
            result = KEYPAD_BUTTONS[row][col]
        except (IndexError, TypeError):
            # Too big index, or row/column = None
            result = None  # If not allowed index or no press
        return result


def keypad_test():
    """Test Keypad Class"""
    keypad = Keypad()
    assert keypad.parse_result(0, 0) == "1"
    assert keypad.parse_result(1, 1) == "5"
    assert keypad.parse_result(2, 2) == "9"
    assert keypad.parse_result(0, 3) == "*"
    assert keypad.parse_result(1, 3) == "0"
    assert keypad.parse_result(2, 3) == "#"
    assert keypad.parse_result(None, None) is None
    assert keypad.parse_result(7, 7) is None
    print("Keypad Parse Test Successful")
    keypad.setup_poll()


if __name__ == "__main__":
    keypad_test()
