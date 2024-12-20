from pynput.keyboard import Key, Controller
import win32gui as wgui
import time

class Ability_Execute:
    @staticmethod
    def Execute_Ability(keybind: str):
        keyboard = Controller()
        keyboard.press(keybind)
        time.sleep(.1)
        keyboard.release(keybind)