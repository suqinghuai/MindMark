# filepath: auto_click.py
# 功能：模拟鼠标点击、键盘输入，完成自动填分和翻页

import time
import pyautogui

# 开启防故障机制：鼠标移到屏幕左上角(0,0)立即抛异常停止
pyautogui.FAILSAFE = True
# 每次操作后的默认暂停时间（秒）
pyautogui.PAUSE = 0.3


def click(x: int, y: int, delay: float = 0.5):
    """
    点击屏幕指定坐标
    :param x: 横坐标
    :param y: 纵坐标
    :param delay: 点击后等待时间
    """
    pyautogui.click(x, y)
    time.sleep(delay)


def input_score(score: int, input_x: int, input_y: int, submit_x: int, submit_y: int, delay: float = 0.5):
    """
    激活分数输入框，清空后输入分数，然后点击提交
    :param score: 要输入的分数
    :param input_x: 输入框x坐标
    :param input_y: 输入框y坐标
    :param submit_x: 提交按钮x坐标
    :param submit_y: 提交按钮y坐标
    :param delay: 操作间隔
    """
    # 点击输入框激活
    click(input_x, input_y, delay)
    # 全选后删除旧内容，再输入新分数
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.press("delete")
    time.sleep(0.2)
    pyautogui.typewrite(str(score), interval=0.05)
    time.sleep(delay)
    # 点击提交按钮
    click(submit_x, submit_y, delay)


def next_question(next_x: int, next_y: int, delay: float = 1.0):
    """
    点击「下一题」按钮
    :param next_x: 下一题按钮x坐标
    :param next_y: 下一题按钮y坐标
    :param delay: 点击后等待页面加载的时间
    """
    click(next_x, next_y, delay)
