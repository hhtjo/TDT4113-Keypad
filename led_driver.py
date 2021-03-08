"""Module containing Led Driver"""
from typing import Iterable
from time import sleep
from GPIOSimulator_v5 import GPIOSimulator

class LedDriver():
    """Led driver class"""
    def __init__(self) -> None:
        self.gpio_sim = GPIOSimulator()
        self.led_lighting_states = (
            ((0, 1, 1), (1, 1, 0)),
            ((1, 1, 1), (0, 1, 0)),
            ((1, 1, 1), (2, 1, 0)),
            ((2, 1, 1), (1, 1, 0)),
            ((0, 1, 1), (2, 1, 0)),
            ((2, 1, 1), (0, 1, 0)),
        )
        self._all_to_input()

    def _all_to_input(self):
        for i in range(0, 6):
            self.gpio_sim.setup(i, 0)

    def _light_diode(self, led):
        states = self.led_lighting_states[led]
        self.gpio_sim.setup(states[0][0], 1)
        self.gpio_sim.setup(states[1][0], 1)
        self.gpio_sim.output(states[0][0], states[0][2])
        self.gpio_sim.output(states[1][0], states[1][2])
        self.gpio_sim.show_leds_states()
        self._all_to_input()

    def _light_sequence(self, sequence: list) -> None:
        for led, state in enumerate(sequence):
            if state:
                self._light_diode(led)
        sleep(0.00001)

    def _light_simult(self, sequence: list, frame_count):
        i = 0
        while i < frame_count:
            self._light_sequence(sequence)
            i += 1

    def _light_anim(self, sequence: Iterable, frame_count: int = 30):
        for frame in sequence:
            self._light_simult(frame, frame_count)

    def power_up(self):
        """Light power up sequence"""
        self._light_anim((
            (1, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0),
            (1, 1, 1, 0, 0, 0),
            (1, 1, 1, 1, 0, 0),
            (1, 1, 1, 1, 1, 0),
            (1, 1, 1, 1, 1, 1)
        ))

    def power_down(self):
        """Light power down sequence"""
        self._light_anim((
            (1, 1, 1, 1, 1, 1),
            (1, 1, 1, 1, 1, 0),
            (1, 1, 1, 1, 0, 0),
            (1, 1, 1, 0, 0, 0),
            (1, 1, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 0),
        ))

    def twinkle(self):
        """Light twinkle sequence"""
        self._light_anim((
            (0, 0, 0, 1, 1, 0),
            (0, 0, 1, 0, 0, 1),
            (1, 0, 1, 1, 0, 0),
            (0, 1, 0, 0, 1, 0),
            (1, 0, 1, 0, 0, 1),
            (0, 1, 0, 0, 1, 0),
            (0, 1, 0, 0, 1, 0),
            (0, 0, 1, 0, 0, 1),
            (1, 0, 1, 1, 0, 0),
            (0, 1, 0, 0, 1, 0),
            (1, 0, 1, 0, 0, 1),
            (0, 1, 0, 0, 1, 0),
        ), 10)

    def flash(self):
        """Light flash sequence"""
        self._light_anim((
            (1, 1, 1, 1, 1, 1),
            (0, 0, 0, 0, 0, 0),
            (1, 1, 1, 1, 1, 1),
            (0, 0, 0, 0, 0, 0),
            (1, 1, 1, 1, 1, 1),
            (0, 0, 0, 0, 0, 0),
            (1, 1, 1, 1, 1, 1),
            (0, 0, 0, 0, 0, 0),
            (1, 1, 1, 1, 1, 1),
            (0, 0, 0, 0, 0, 0),
            (1, 1, 1, 1, 1, 1),
            (0, 0, 0, 0, 0, 0),
        ), 10)

    def light_single(self, led: int, dur: float):
        """Light single LED"""
        self._light_diode(led)
        sleep(dur)
        self._all_to_input()
        self.gpio_sim.show_leds_states()


def main():
    """main func"""
    ld_driver = LedDriver()
    ld_driver.light_single(2, 1)


if __name__ == "__main__":
    main()
