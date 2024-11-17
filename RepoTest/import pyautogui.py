import cv2
import numpy as np
import pyautogui
import time

time.sleep(3)

# Path to the image you want to find
IMAGE_PATH = r'C:\Users\potte\OneDrive\Desktop\OSRSTreePNG.PNG'  # Make sure this path is correct

# Take a screenshot of the screen using pyautogui
screenshot = pyautogui.screenshot()

# Convert screenshot from RGB (PIL) to BGR (OpenCV format)
screenshot = np.array(screenshot)  # Convert to NumPy array
screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR

# Load the image you want to search for (template)
template = cv2.imread(IMAGE_PATH)

# Check if the template was loaded correctly
if template is None:
    print(f"Error: Template image could not be loaded from {IMAGE_PATH}")
    exit()

# Convert both the screenshot and the template to grayscale
screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Perform template matching on grayscale images
result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# Get the locations of the matches
threshold = 0.4  # Minimum match confidence (adjust as needed)
locations = np.where(result >= threshold)

# If we find a match, draw a rectangle around each match and click on the best match
if len(locations[0]) > 0 and len(locations[1]) > 0:
    print(f"Found {len(locations[0])} matches.")
    
    # Draw rectangles around each match for debugging
    for pt in zip(*locations[::-1]):  # Locations are in (y, x) format, so we reverse them
        top_left = pt
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)  # Draw a green rectangle

    # Show the result with drawn rectangles (optional)
    #cv2.imshow("Matches", screenshot)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Use cv2.minMaxLoc to find the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # The best match is where the maximum value is
    best_match = max_loc
    center = (best_match[0] + template.shape[1] // 2, best_match[1] + template.shape[0] // 2)
    print(f"Clicking on best match at: {center}")
    
    # Click on the center of the best match
    time.sleep(2)
    pyautogui.click(center)
else:
    print("Image not found on the screen.")
