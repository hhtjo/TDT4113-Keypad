"""Module containing KPC Agent"""
import re
from keypad import Keypad
from led_driver import LedDriver


class KpcAgent:
    """Keypad Controller Agent Class"""

    def __init__(self) -> None:
        self.keypad = Keypad()
        self.leds = LedDriver()
        self.override_signal = None
        self.entry_buffer = ""
        self.passcode = "1234"

    def reset_passcode_entry(self):
        """Resets current entered passcode"""
        self.entry_buffer = ""

    def receive_signal(self, signal):
        """Receive signal from FSM"""
        self.entry_buffer += signal

    def get_next_signal(self):
        """Get next signal from Keypad"""
        if self.override_signal:
            return self.override_signal
        return self.keypad.get_next_signal()

    def verify_login(self):
        """Verify passcode"""
        return self.entry_buffer == self.passcode

    def validate_passcode_change(self):
        """Validate new passcode"""
        if re.search(r"[^\d]", self.passcode):
            self.set_new_passcode(self.passcode)

    def set_new_passcode(self, new_passcode):
        """Sets new passcode"""
        with open('passcode.txt', 'w') as pass_file:
            pass_file.write(new_passcode)

    def read_passcode(self):
        """Reads passcode from file"""

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
