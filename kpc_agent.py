"""Module containing KPC Agent"""
from keypad import Keypad
from led_driver import LedDriver


class KpcAgent:
    """Keypad Controller Agent Class"""

    def __init__(self) -> None:
        self.keypad = Keypad()
        self.leds = LedDriver()
        self.override_signal = None
        self.entry_buffer = ""
        self.passcode = None

    def light_led(self, duration):
        """Light led from buffer"""
        led = int(self.entry_buffer)
        duration = int(duration)
        if 6 < led >= 0:
            self.light_one_led(led, duration)
        self.reset_buffer()

    def power_down(self):
        """Power down"""
        self.reset_buffer()
        self.leds.power_down()

    def wakeup(self):
        """Power up system"""
        self.leds.power_up()

    def reset_buffer(self):
        """Resets current entered passcode"""
        self.entry_buffer = ""

    def fsm_signal(self, signal):
        """Receive signal from FSM"""
        self.entry_buffer += signal

    def get_next_signal(self):
        """Get next signal from Keypad"""
        return_signal = None
        if self.override_signal:
            return_signal = self.override_signal
            self.override_signal = None
        else:
            return_signal = self.keypad.get_next_signal()
        return return_signal

    def verify_login(self):
        """Verify passcode"""
        print(self.entry_buffer)
        print(self.read_passcode())
        if self.entry_buffer == self.read_passcode():
            self.override_signal = "Y"
            self.twinkle_leds()
        else:
            self.override_signal = "N"
            self.flash_leds()
        self.entry_buffer = ""

    def validate_passcode_change(self):
        """Validate new passcode"""
        passcodes = self.entry_buffer.split('*')
        # if not re.search(r"[^\d]", self.passcode[0]):
        if passcodes[0] == passcodes[1]:
            self.set_new_passcode(passcodes[0])
        else:
            self.twinkle_leds()
        self.reset_buffer()

    def set_new_passcode(self, new_passcode):
        """Sets new passcode"""
        with open('passcode.txt', 'w') as pass_file:
            pass_file.write(new_passcode)
            self.passcode = new_passcode

    def read_passcode(self):
        """Reads passcode from file"""
        if not self.passcode:
            with open('passcode.txt') as pass_file:
                self.passcode = pass_file.readline().strip()
        return self.passcode

    def light_one_led(self, led, duration):
        """Light specific LED"""
        self.leds.light_single(led, duration)

    def flash_leds(self):
        """Flash all LEDs"""
        self.leds.flash()

    def twinkle_leds(self):
        """Twinkle all LEDs"""
        self.leds.twinkle()

    def exit_action(self):
        """Power Down LEDs"""
        self.leds.power_down()


KPC_INSTANCE = KpcAgent()
