import os
import ctypes
import pyautogui
import screen_brightness_control as sbc
import io
from PIL import Image
import win32clipboard


# ---------------- VOLUME ----------------

def volume_up():
    for _ in range(5):
        pyautogui.press("volumeup")
    return "Volume increased"


def volume_down():
    for _ in range(5):
        pyautogui.press("volumedown")
    return "Volume decreased"


def mute():
    pyautogui.press("volumemute")
    return "Muted"


def unmute():
    pyautogui.press("volumemute")
    return "Unmuted"


# ---------------- BRIGHTNESS ----------------

def brightness_up():
    try:
        current = sbc.get_brightness()[0]
        sbc.set_brightness(min(100, current + 10))
        return "Brightness increased"
    except:
        return "Brightness control not supported"


def brightness_down():
    try:
        current = sbc.get_brightness()[0]
        sbc.set_brightness(max(0, current - 10))
        return "Brightness decreased"
    except:
        return "Brightness control not supported"


# ---------------- SCREENSHOT ----------------

def screenshot():
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    if not os.path.exists(desktop):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    path = os.path.join(desktop, "screenshot.png")
    img = pyautogui.screenshot()
    img.save(path)

    # copy to clipboard
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    return f"Screenshot saved and copied to clipboard"
    

# ---------------- POWER ----------------

def shutdown_pc():
    os.system("shutdown /s /t 5")
    return "Shutting down in 5 seconds"


def restart_pc():
    os.system("shutdown /r /t 5")
    return "Restarting in 5 seconds"


def lock_screen():
    ctypes.windll.user32.LockWorkStation()
    return "Locked"