import cv2 as cv
import numpy as np
import pyscreenshot as ImageGrab
import time
import pyautogui

def find_mask_on_screen(mask_path, threshold=0.85):
    screen = np.array(ImageGrab.grab()).astype(np.uint8)
    screen = screen[:,:int(screen.shape[1]*0.77)]
    screen = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)  # Convert to grayscale

    template = cv.imread(mask_path, cv.IMREAD_GRAYSCALE).astype(np.uint8)
    result = cv.matchTemplate(screen, template, cv.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)
    high_correlation_points = list(zip(*locations[::-1]))  # (x, y) format

    return high_correlation_points, result

def skip_ad():
    high_correlation_points, result = find_mask_on_screen("2_block_mask.png", 0.80)
    clicking_point = [high_correlation_points[0][0] + 80, high_correlation_points[0][1] + 90]
    pyautogui.click(clicking_point[0], clicking_point[1])

    time.sleep(0.15)
    high_correlation_points = []
    while len(high_correlation_points) == 0:
        high_correlation_points, result = find_mask_on_screen("3_confirmation_mask.png", 0.75)
        clicking_point = [high_correlation_points[0][0] + 570, high_correlation_points[0][1] + 200]
        pyautogui.click(clicking_point[0], clicking_point[1])
        time.sleep(0.2)
        clicking_point = [high_correlation_points[0][0] - 40, high_correlation_points[0][1]  -40]
        pyautogui.click(clicking_point[0], clicking_point[1])

while True:
    try:
        time.sleep(1)
        skip_ad()
    except:
        pass
