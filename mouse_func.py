import win32api, win32con
from time import sleep
import random


def mouseLeftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 按下
    sleep(random.random() * 0.05 + 0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 抬起


def mouseRightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  # 按下
    sleep(random.random() * 0.05 + 0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)  # 抬起


def mouseMove(dx, dy):
    sleep(random.random() * 0.05 + 0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)  # 移动鼠标到相对位置


def mouseMoveTo(x, y):
    sleep(random.random() * 0.05 + 0.05)
    win32api.SetCursorPos((x, y))  # 移动鼠标到指定位置


def mouseClick(x, y):
    mouseMoveTo(x, y)
    mouseLeftClick()
