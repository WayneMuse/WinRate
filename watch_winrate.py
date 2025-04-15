import pyautogui
import cv2
import numpy as np
import time
import keyboard
import pygetwindow as gw
import os

# Set the working directory to where the images are
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load all template images
templates = {
    "winrate": cv2.imread('winrate.png', cv2.IMREAD_UNCHANGED),
    "speech_menu": cv2.imread('Speech Menu.png', cv2.IMREAD_UNCHANGED),
    "fast_forward": cv2.imread('Fast Forward.png', cv2.IMREAD_UNCHANGED),
    "confirm": cv2.imread('Confirm.png', cv2.IMREAD_UNCHANGED)
}

# Convert templates to grayscale
templates_gray = {
    name: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for name, img in templates.items()
}

# Set match threshold
threshold = 0.8

# Template dimensions
template_sizes = {
    name: img.shape[::-1][1::-1]  # (w, h)
    for name, img in templates_gray.items()
}

def get_active_window_title():
    try:
        win = gw.getActiveWindow()
        return win.title if win else ""
    except Exception:
        return ""

def find_image_center(screen_gray, template_gray):
    result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        w, h = template_gray.shape[::-1]
        return (pt[0] + w // 2, pt[1] + h // 2)
    return None

def click_image_center(image_name, screen_gray):
    center = find_image_center(screen_gray, templates_gray[image_name])
    if center:
        pyautogui.moveTo(center)
        pyautogui.click()
        print(f"Clicked {image_name} at {center}")
        time.sleep(0.5)
        return True
    return False

print("Watching for actions in LimbusCompany...")

while True:
    title = get_active_window_title()

    if "LimbusCompany" in title:
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        # Check WinRate first
        winrate_found = find_image_center(screenshot_gray, templates_gray["winrate"])
        if winrate_found:
            print("WinRate detected. Sending 'p' and 'enter'.")
            time.sleep(.25)
            keyboard.press_and_release('p')
            time.sleep(0.25)
            keyboard.press_and_release('enter')
            #break

        # Check for Speech Menu chain
        speech_found = find_image_center(screenshot_gray, templates_gray["speech_menu"])
        if speech_found:
            print("Speech Menu detected. Clicking sequence...")
            pyautogui.moveTo(speech_found)
            pyautogui.click()
            time.sleep(0.5)

            # Update screen after each action
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

            click_image_center("fast_forward", screenshot_gray)

            # Update again
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

            click_image_center("confirm", screenshot_gray)
            print("Finished speech menu sequence.")

    time.sleep(1)
