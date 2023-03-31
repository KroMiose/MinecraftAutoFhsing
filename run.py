import pyautogui as gui
from mouse_func import *
from Zone import Zone
import sys, win32gui

import pyglet
import keyboard
from key_func import *
from threading import Thread

from time import sleep


# region ==================== 配置区 ====================
tick = 0.3  # 运行检测间隔 单位：秒 (越小越精确，过小可能导致误判)
starHookCheckTime = 3  # 抛竿后开始检测延迟 单位：秒 (防止误判)
autoSwitch = True  # 是否自动切换钓竿   True：自动切换   False：不自动切换
checkStep = 2  # 检测步长 单位：像素 (越小越精确，但是越慢)
# endregion

# region ==================== 全局变量 ====================
scriptName = "MinecraftAutoFhsing  by:KroMiose"  # 脚本名
scriptDescript = """
执行脚本请打开游戏窗口化并且最大化

提示：按下 ~ 可以切换脚本运行开关
"""

windowHWND = None  # 游戏窗口句柄
runStatus = False  # 脚本运行状态
windowRect = None  # 游戏窗口位置
checkRect = None  # 检测区域

gotFish = True  # 是否钓到鱼
fishCnt = 0     # 钓到鱼次数
scanCnt = 0     # 扫描次数
errCnt = 0      # 错误次数
changeCnt = 0   # 切换次数
tickCnt = 0     # 计时器
warnCnt = 0     # 警告次数
# endregion

# 创建层叠窗口
def creatCasWindow():
    config = pyglet.gl.Config(double_buffer=True, depth_size=24, alpha_size=8)
    window = pyglet.window.Window(windowRect[2], windowRect[3],
                    vsync=False, style='overlay', config=config,
                    caption="MinecraftAutoFishingRECT")
    window.set_location(windowRect[0], windowRect[1])

    # 设为顶层窗口
    win32gui.SetWindowPos(window._hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    # 切换激活窗口为游戏
    win32gui.SetForegroundWindow(windowHWND)

    @window.event
    def on_draw():
        global runStatus, checkRect
        window.clear()
        window.set_location(windowRect[0], windowRect[1])
        window.set_size(windowRect[2], windowRect[3])

        showText = f"自动钓鱼：{'开启' if runStatus else '关闭'} | 钓到的鱼: {fishCnt} (预估)"
        rectColor = (50, 233, 50)
        pyglet.text.Label(showText, x=windowRect[2] - 300, y=24).draw()
        # 框出检测区域
        if runStatus and (checkRect is not None):
            # 计算四条边线段坐标 (Y轴坐标需要反转)
            x1, y1, x2, y2 = checkRect[0], windowRect[3] - checkRect[1], checkRect[0] + checkRect[2], windowRect[3] - (checkRect[1] + checkRect[3])
            # 绘制四条边线段
            pyglet.shapes.Line(x1, y1, x1, y2, width=1, color=rectColor).draw()
            pyglet.shapes.Line(x1, y2, x2, y2, width=1, color=rectColor).draw()
            pyglet.shapes.Line(x2, y2, x2, y1, width=1, color=rectColor).draw()
            pyglet.shapes.Line(x2, y1, x1, y1, width=1, color=rectColor).draw()

    pyglet.app.run(interval=1/30)

# 获取浮标位置
def getHookLocation():
    global checkRect
    # 计算浮标检测区域
    width, height = 50, windowRect[3] / 3
    x, y = windowRect[0] + windowRect[2] / 2 - width / 2, windowRect[1] + windowRect[3] / 2 + 10
    checkRect = (x, y, width, height)
    zone = Zone(x, y, width, height)
    res = zone.findColorRangeExist(rmin=100, gmax=60, bmax=60)
    # print(f"浮标检测结果：{res}")
    return res

# 运行动作
def doSthInRunning():
    global errCnt, changeCnt, gotFish, fishCnt, tickCnt, scanCnt, warnCnt
    # print(f"tickCnt: {tickCnt}")
    if getHookLocation() is False:  # 未检测到浮标
        if errCnt > 0:
            print(f"异常值：{errCnt}")
        if autoSwitch & (errCnt > 4):  # 错误发生次数大于4次
            gui.scroll(-500)
            changeCnt += 1
            print(f"检测到鱼竿异常，自动切换钓竿，切换次数：{changeCnt}")
            errCnt = 0
            warnCnt = 0
            gotFish = True
        if warnCnt > 2:
            print("布尔状态异常~自动修正")
            gotFish = not gotFish
            fishCnt -= 3
            warnCnt = 0
        if gotFish == False:  # 未钓到鱼
            gui.click(button="right")
            sleep(1)
            fishCnt += 1
            print(f"检测到浮标变化，钓到的鱼: {fishCnt}（预计） 扫描次数：f{scanCnt}")
            if scanCnt < 2:
                warnCnt += 1
                errCnt += 1
            else:
                warnCnt = 0
                errCnt = 0
            gotFish = True
            scanCnt = 0
            changeCnt = 0
        if changeCnt > 9:
            print("你的钓竿已用完，自动结束脚本！")
            return
        if gotFish:
            gui.click(button="right")
            print("执行抛竿~")
            gotFish = False
            sleep(starHookCheckTime)
    else:  # 检测到浮标
        scanCnt += 1
        gotFish = False
        errCnt = 0

# 暂停动作
def doWhenStop():
    global errCnt, warnCnt, gotFish
    errCnt, warnCnt = 0, 0
    gotFish = True

# 键盘监听线程
def checkKeyboardThread():
    global runStatus
    while True:
        keyboard.wait('`')
        runStatus = not runStatus

def main():
    global windowRect, windowHWND
    print(f"脚本：{scriptName}")
    print(f"说明：{scriptDescript}")
    print('请手动切换到游戏窗口，然后按下F10键，程序将自动获取窗口句柄\n')
    keyboard.wait('F10')
    # 获取窗口位置和大小
    windowHWND = win32gui.GetForegroundWindow()
    windowRect = win32gui.GetWindowRect(windowHWND)
    print(f"获取到窗口句柄：{windowHWND}，窗口区域：{windowRect} 开始运行脚本")

    # 启动键盘检测线程
    keyboardThread = Thread(target=checkKeyboardThread, daemon=True)
    keyboardThread.start()

    # 主循环
    def runLoop():
        global runStatus, tickCnt
        runStatus = False
        while True:
            lastRunStatus = runStatus
            if runStatus == True:  # 脚本运行
                if runStatus != lastRunStatus:  # 脚本刚刚开始运行
                    print("脚本开始运行~")
                doSthInRunning()

            else:  # 脚本暂停
                if runStatus != lastRunStatus:  # 脚本刚刚暂停
                    print("脚本暂停中~")
                    doWhenStop()

            sleep(tick)
            tickCnt += 1

    # 启动主循环
    Thread(target=runLoop, daemon=True).start()

    # 创建层叠窗口
    creatCasWindow()


if __name__ == "__main__":
    sys.exit(main())