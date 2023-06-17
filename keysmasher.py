#!/usr/bin/env python3

import argparse
import subprocess
from time import sleep
from enum import Enum
import re


class KeyState(Enum):
    UP = 1
    DOWN = 2


class Smasher:
    def __init__(self, delay, device_id) -> None:
        self._delay = delay
        self._device_id = device_id
        self._layout = self._get_xmodmap_layout()
        self._reversed_layout = {v: k for k, v in self._layout.items()}

    @staticmethod
    def __match_key(key) -> tuple:
        pattern = r'keycode\s*(?P<keycode>\d*)\s*=[\r\t\f ](?P<key>\b\w{1})\s'
        match = re.match(pattern, key)

        if not match:
            return None

        keycode = int(match.group('keycode'))
        key = match.group('key')

        return (keycode, key)

    def _get_xmodmap_layout(self) -> dict:
        result = subprocess.run(
            ['xmodmap', '-pke'],
            stdout=subprocess.PIPE,
            check=False,
        )

        keys = result.stdout.decode().split('\n')
        keys = [self.__match_key(key) for key in keys]
        keys = [key for key in keys if key is not None]

        return dict(keys)

    def get_scancode(self, key) -> int:
        return self._reversed_layout[key]

    def get_key(self, scancode) -> str:
        return self._layout[scancode]

    @staticmethod
    def __match_key_status(key) -> tuple:
        pattern = r'key\[(?P<keycode>\d*)\]=(?P<status>.*)'
        match = re.match(pattern, key)

        if not match:
            return None

        keycode = int(match.group('keycode'))
        status = KeyState.UP if match.group(
            'status') == 'up' else KeyState.DOWN

        return (keycode, status)

    def get_key_state(self, key) -> KeyState:
        return self.get_keyboard_state()[self.get_scancode(key)]

    def get_keyboard_state(self) -> dict:
        result = subprocess.run(
            ['xinput', '--query-state', str(self._device_id)],
            stdout=subprocess.PIPE,
            check=False,
        )

        keys = result.stdout.decode().split()
        keys = [self.__match_key_status(key) for key in keys]
        keys = [key for key in keys if key is not None]

        return dict(keys)

    @staticmethod
    def press_key(key):
        subprocess.run(
            ['xdotool', 'key', key],
            check=False,
        )

    def smash_key(self, key):
        while self.get_key_state(key) == KeyState.DOWN:
            self.press_key(key)
            sleep(self._delay)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--delay", help="delay between keypresses in msecs", type=int, required=True)
parser.add_argument("-i", "--device-id",
                    help="id of keyboard device (use xinput --list)", type=int, required=True)
parser.add_argument("-k", "--keys", nargs='+',
                    help="keys to be smashed", required=True)

args = parser.parse_args()

smasher = Smasher(delay=args.delay / 1000, device_id=args.device_id)

while True:
    for k in args.keys:
        smasher.smash_key(k)
