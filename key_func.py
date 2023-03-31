import win32api, win32con
from time import sleep
import random


keys = {"a": 65,"b": 66,"c": 67,"d": 68,"e": 69,"f": 70,"g": 71,"h": 72,"i": 73,"j": 74,"k": 75,"l": 76,"m": 77,"n": 78,"o": 79,"p": 80,"q": 81,"r": 82,"s": 83,"t": 84,"u": 85,"v": 86,"w": 87,"x": 88,"y": 89,"z": 90,"0": 48,"1": 49,"2": 50,"3": 51,"4": 52,"5": 53,"6": 54,"7": 55,"8": 56,"9": 57,}

def keydownup(key):
    sleep(random.random() * 0.1)
    win32api.keybd_event(key, win32api.MapVirtualKey(key, 0), 0, 0)
    sleep(random.random() * 0.1 + 0.05)
    win32api.keybd_event(
        key, win32api.MapVirtualKey(key, 0), win32con.KEYEVENTF_KEYUP, 0
    )


def keydown(key):
    win32api.keybd_event(key, win32api.MapVirtualKey(key, 0), 0, 0)


def keyup(key):
    win32api.keybd_event(
        key, win32api.MapVirtualKey(key, 0), win32con.KEYEVENTF_KEYUP, 0
    )