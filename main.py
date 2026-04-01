import mss
import mss.tools
import keyboard
import pygetwindow as gw
import os
import time
import threading

SAVE_FOLDER = "screenshots"
MODE = "full"

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


def save_png(img, size, filename):
    mss.tools.to_png(img.rgb, size, output=filename)


def capture_full():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        img = sct.grab(monitor)

        filename = f"{SAVE_FOLDER}/full_{time.time_ns()}.png"

        threading.Thread(
            target=save_png,
            args=(img, img.size, filename),
            daemon=True
        ).start()


def capture_window():

    win = gw.getActiveWindow()

    if win is None:
        return

    bbox = {
        "top": win.top,
        "left": win.left,
        "width": win.width,
        "height": win.height
    }

    if bbox["width"] <= 0 or bbox["height"] <= 0:
        return

    with mss.mss() as sct:

        img = sct.grab(bbox)

        filename = f"{SAVE_FOLDER}/window_{time.time_ns()}.png"

        threading.Thread(
            target=save_png,
            args=(img, img.size, filename),
            daemon=True
        ).start()


def capture():

    if MODE == "full":
        capture_full()

    if MODE == "window":
        capture_window()


def set_full():
    global MODE
    MODE = "full"
    print("Mode: FULL")


def set_window():
    global MODE
    MODE = "window"
    print("Mode: WINDOW")


def exit_program():
    print("Exit")
    os._exit(0)


print("==============")
print("SCREENSHOT TOOL")
print("==============")
print("1 → Full screen")
print("2 → Window")
print("SPACE → Capture")
print("ESC → Exit")
print("==============")

keyboard.add_hotkey("1", set_full)
keyboard.add_hotkey("2", set_window)
keyboard.add_hotkey("s", capture)
keyboard.add_hotkey("esc", exit_program)

keyboard.wait()