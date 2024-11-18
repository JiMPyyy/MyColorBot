import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw  # Import pygetwindow to interact with windows
import random  # For random delays
import keyboard  # For detecting key press (e.g., Q)

# Sleep for a few seconds before the script starts to give time to focus the game
time.sleep(3)

# Path to the image you want to find
IMAGE_PATH = r'C:\Users\potte\OneDrive\Desktop\OSRSTreePNG.PNG'  # Make sure this path is correct

# Function to focus on the game window before clicking
def focus_game_window():
    try:
        # Get the window by title (replace with the correct window title of your game)
        window = gw.getWindowsWithTitle("RuneLite - Lolwhatami")[0]  # Replace with the exact title of your game window

        # Activate (bring to front) and maximize the window
        window.activate()
        #window.maximize()

        # Wait for a moment to ensure it's focused before clicking
        time.sleep(1.5)
    except IndexError:
        print("Error: Could not find the game window. Make sure the game is running and the title is correct.")
        exit()

# Function to find and click the tree image with a longer click
def find_and_click_tree():
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
        return

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
        
        # Focus the game window before clicking
        focus_game_window()
        
        # Ensure the game window is focused before clicking
        time.sleep(0.5)

        # Simulate the "press-and-hold" mouse click (longer click)
        pyautogui.moveTo(center)  # Move the mouse to the target location
        pyautogui.mouseDown()  # Press the mouse button down
        time.sleep(1)  # Hold the mouse button for 1 second (adjust as needed)
        pyautogui.mouseUp()  # Release the mouse button
        
        # Add a short delay after the click to ensure it's registered
        time.sleep(0.5)
    else:
        print("Image not found on the screen.")

# Main loop to repeatedly search and click with random delays
def main():
    while True:
        # Check if the 'Q' key is pressed, if so, break the loop and stop the script
        if keyboard.is_pressed('q'):  # 'q' to quit
            print("Exiting the script...")
            break
        
        find_and_click_tree()  # Perform the image search and click

        # Randomly sleep between 15 to 30 seconds
        random_delay = random.uniform(10, 20)
        print(f"Waiting for {random_delay:.2f} seconds...")
        time.sleep(random_delay)  # Sleep for a random amount of time between 15 and 30 seconds

if __name__ == "__main__":
    main()
