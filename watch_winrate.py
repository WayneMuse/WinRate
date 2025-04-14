import pyautogui
import cv2
import numpy as np
import time
import keyboard

# Load the reference image
template = cv2.imread('winrate.png', cv2.IMREAD_UNCHANGED)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
w, h = template_gray.shape[::-1]

# Match threshold (you can tweak this if needed)
threshold = 0.8

print("Looking for Win Rate... Press Ctrl+C to exit.")

while True:
    # Capture the screen
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        print("Win Rate detected!")
        keyboard.press_and_release('p')
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        #break
        print("Looking for Win Rate...")

    time.sleep(1)  # Wait a bit before checking again
