import pyautogui
import time

try:
    # Take a screenshot and display it
    screenshot = pyautogui.screenshot()
    screenshot.show()
    print("PyAutoGUI and Pillow are working correctly!")
except Exception as e:
    print(f"An error occurred: {e}")