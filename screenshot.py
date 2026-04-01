# filepath: screenshot.py
# 功能：对屏幕指定区域截图，保存并返回base64编码

import os
import base64
from datetime import datetime
from mss import mss
from PIL import Image
import io


def capture_region(region: dict, save_dir: str = "screenshot") -> tuple:
    """
    对屏幕指定区域截图
    :param region: 截图区域 {"left": x, "top": y, "width": w, "height": h}
    :param save_dir: 截图保存文件夹
    :return: (保存路径, base64编码字符串)，失败返回 (None, None)
    """
    # 自动创建保存文件夹
    os.makedirs(save_dir, exist_ok=True)

    # 用时间戳命名，避免重复
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"cap_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)

    try:
        # mss截图
        with mss() as sct:
            monitor = {
                "left": region["left"],
                "top": region["top"],
                "width": region["width"],
                "height": region["height"],
            }
            screenshot = sct.grab(monitor)

        # 转为PIL图片并保存
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save(filepath, "PNG")

        # 转base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return filepath, img_base64

    except Exception as e:
        print(f"[截图失败] {e}")
        return None, None
