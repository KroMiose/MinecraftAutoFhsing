import pyautogui as gui


class Zone:
    x = None  # 区域开始x坐标
    y = None  # 区域开始y坐标
    w = None  # 区域宽度
    h = None  # 区域高度
    pixCnt = 0  # 区域像素数量

    # 点击区域中心
    def click(self):
        gui.click(x=self.x + self.w / 2, y=self.y + self.h / 2)

    # 获取区域平均色值
    def getAvgColor(self, step=1):
        c0, c1, c2 = 0, 0, 0
        shot = gui.screenshot(region=(self.x, self.y, self.w, self.h))
        for i in range(0, self.w, step):
            for j in range(0, self.h, step):
                pix = shot.getpixel(xy=(i, j))
                c0 += pix[0]
                c1 += pix[1]
                c2 += pix[2]
        c0 /= self.pixCnt
        c1 /= self.pixCnt
        c2 /= self.pixCnt
        return (c0, c1, c2)

    # 检测某像素色值是否存在，offset为偏差允许值
    def findColorExist(self, color, offset, step=1):
        shot = gui.screenshot(region=(self.x, self.y, self.w, self.h))
        for i in range(0, self.w, step):
            for j in range(0, self.h, step):
                pix = shot.getpixel(xy=(i, j))
                if (
                    (abs(pix[0] - color[0]) < offset)
                    & (abs(pix[1] - color[1]) < offset)
                    & (abs(pix[2] - color[2]) < offset)
                ):
                    return pix
        return False

    # 检测某像素范围色值是否存在
    def findColorRangeExist(self, rmin=0, rmax=255, gmin=0, gmax=255, bmin=0, bmax=255, step=1):
        shot = gui.screenshot(region=(self.x, self.y, self.w, self.h))
        for i in range(0, self.w, step):
            for j in range(0, self.h, step):
                pix = shot.getpixel(xy=(i, j))
                if (
                    (pix[0] >= rmin)
                    & (pix[0] <= rmax)
                    & (pix[1] >= gmin)
                    & (pix[1] <= gmax)
                    & (pix[2] >= bmin)
                    & (pix[2] <= bmax)
                ):
                    return pix
        return False

    # 检测某像素色值是否不存在，offset为偏差允许值
    def checkColorNoExist(self, color, offset):
        return True if self.findColorExist(color, offset) == False else False

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = int(x), int(y), int(w), int(h)
        self.pixCnt = w * h