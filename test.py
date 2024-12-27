import cv2
import pyautogui
import numpy as np
import time

def locate_and_click_button(button_image_path):
    # Take a screenshot of all monitors
    screenshot = pyautogui.screenshot()
    # Convert the screenshot to a numpy array
    screenshot_np = np.array(screenshot)
    # Convert from RGB to BGR for OpenCV
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    # Read the button image
    button_image = cv2.imread(button_image_path, cv2.IMREAD_UNCHANGED)
    if button_image is None:
        print(f"Error: Button image not found at {button_image_path}")
        return
    # Ensure both images are in the same format
    if len(button_image.shape) == 2:  # If button image is single-channel
        screenshot_bgr = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
    elif button_image.shape[2] == 4:  # If button image has an alpha channel
        button_image = cv2.cvtColor(button_image, cv2.COLOR_BGRA2BGR)
    # Match the template
    result = cv2.matchTemplate(screenshot_bgr, button_image, cv2.TM_CCOEFF_NORMED)
    # Find the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # Define a threshold for a match
    threshold = 0.8  # Adjust based on your needs
    if max_val >= threshold:
        # Calculate the center of the button
        button_w, button_h = button_image.shape[1], button_image.shape[0]
        center_x = max_loc[0] + button_w // 2
        center_y = max_loc[1] + button_h // 2
        # Move the mouse and click
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        print(f"Clicked at {center_x}, {center_y}")
    else:
        print("Button not found")

def check_and_click_error_button(error_image_path, ok_button_image_path):
    # Take a screenshot of all monitors
    screenshot = pyautogui.screenshot()
    # Convert the screenshot to a numpy array
    screenshot_np = np.array(screenshot)
    # Convert from RGB to BGR for OpenCV
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    # Read the error image
    error_image = cv2.imread(error_image_path, cv2.IMREAD_UNCHANGED)
    if error_image is None:
        print(f"Error: Error image not found at {error_image_path}")
        return False
    # Ensure both images are in the same format
    if len(error_image.shape) == 2:  # If error image is single-channel
        screenshot_bgr = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
    elif error_image.shape[2] == 4:  # If error image has an alpha channel
        error_image = cv2.cvtColor(error_image, cv2.COLOR_BGRA2BGR)
    # Match the template
    result = cv2.matchTemplate(screenshot_bgr, error_image, cv2.TM_CCOEFF_NORMED)
    # Find the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # Define a threshold for a match
    threshold = 0.8  # Adjust based on your needs
    if max_val >= threshold:
        print("Error message found")
        # Locate and click the OK button
        locate_and_click_button(ok_button_image_path)
        return True
    else:
        print("Error message not found")
        return False

# Path to the images of the buttons
button_image_path_1 = "button1.png"  # Replace with the path to your first button image
button_image_path_2 = "button2.png"  # Replace with the path to your second button image
error_image_path = "error.png"  # Replace with the path to your error message image
ok_button_image_path = "ok_button.png"  # Replace with the path to your OK button image

# Wait for the screen to load
time.sleep(2)

# Repeat the process 5 times
for _ in range(5):
    # Locate and click the first button
    locate_and_click_button(button_image_path_1)
    # Wait for a short duration before clicking the second button
    time.sleep(2)
    # Locate and click the second button
    locate_and_click_button(button_image_path_2)
    # Wait for a short duration before repeating
    time.sleep(10)
    # Check for error message and click OK button if found
    if check_and_click_error_button(error_image_path, ok_button_image_path):
        # Wait for 60 seconds if error message was found and OK button clicked
        time.sleep(600)
