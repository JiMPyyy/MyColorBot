import pyautogui
import cv2
import numpy as np
import time
import pygetwindow as gw
import random
import keyboard

# Sleep for a few seconds before the script starts to give time to focus the game
time.sleep(3)

# Path to the image you want to find (Tree image)
IMAGE_PATH = r'C:\Users\potte\OneDrive\Desktop\OSRSTreePNG.PNG'  # Make sure this path is correct

# Path to inventory slot reference image (you can create this using screenshot of a full inventory slot)
INVENTORY_SLOT_PATH = r'C:\Users\potte\OneDrive\Desktop\FullInventory.png'

# Global variables for manually defined regions
tree_region = (50, 25, 800, 800)  # Example (x, y, width, height) for the tree region
inventory_region = (900, 100, 400, 800)  # Example (x, y, width, height) for the inventory region

# Function to focus on the game window before clicking
def focus_game_window():
    try:
        # Get the window by title (replace with the correct window title of your game)
        window = gw.getWindowsWithTitle("RuneLite - Lolwhatami")[0]  # Replace with the exact title of your game window
        # Activate (bring to front) and maximize the window
        window.activate()
        # Wait for a moment to ensure it's focused before clicking
        time.sleep(1.5)
    except IndexError:
        print("Error: Could not find the game window. Make sure the game is running and the title is correct.")
        exit()

# Function to find and click the tree image with a longer click
def find_and_click_tree():
    if tree_region is None:
        print("Tree region is not defined.")
        return

    # Take a screenshot of the screen using pyautogui
    screenshot = pyautogui.screenshot()

    # Convert screenshot from RGB (PIL) to BGR (OpenCV format)
    screenshot = np.array(screenshot)  # Convert to NumPy array
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR

    # Crop the image to the selected tree region
    tree_screenshot = screenshot[tree_region[1]:tree_region[1] + tree_region[3], tree_region[0]:tree_region[0] + tree_region[2]]

    # Load the image you want to search for (template)
    template = cv2.imread(IMAGE_PATH)

    # Check if the template was loaded correctly
    if template is None:
        print(f"Error: Template image could not be loaded from {IMAGE_PATH}")
        return

    # Convert both the screenshot and the template to grayscale
    tree_screenshot_gray = cv2.cvtColor(tree_screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Perform template matching on grayscale images
    result = cv2.matchTemplate(tree_screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Get the locations of the matches
    threshold = 0.4  # Minimum match confidence (adjust as needed)
    locations = np.where(result >= threshold)

    # If we find a match, draw a rectangle around each match and click on the best match
    if len(locations[0]) > 0 and len(locations[1]) > 0:
        print(f"Found {len(locations[0])} matches.")

        # Use cv2.minMaxLoc to find the best match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # The best match is where the maximum value is
        best_match = max_loc
        center = (best_match[0] + tree_region[0] + template.shape[1] // 2, 
                  best_match[1] + tree_region[1] + template.shape[0] // 2)
        
        print(f"Best match at: {best_match}")
        print(f"Clicking on center: {center}")

        # Focus the game window before clicking
        focus_game_window()
        
        # Ensure the game window is focused before clicking
        time.sleep(0.5)

        # Simulate the "click" instead of press-and-hold
        pyautogui.moveTo(center)  # Move the mouse to the target location
        time.sleep(0.2)  # Small delay before click (to ensure the mouse moves smoothly)
        pyautogui.click()  # Perform the click action
        
        # Add a short delay after the click to ensure it's registered
        time.sleep(0.5)
    else:
        print("Image not found on the screen.")

# Function to drop items from the inventory when full
def drop_items_from_inventory():
    # Take a screenshot of the inventory region
    screenshot = pyautogui.screenshot(region=inventory_region)
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # Convert the screenshot to grayscale

    # Load the inventory slot image in grayscale
    inventory_slot_template = cv2.imread(INVENTORY_SLOT_PATH, cv2.IMREAD_GRAYSCALE)

    # Check if the template was loaded correctly
    if inventory_slot_template is None:
        print(f"Error: Template image could not be loaded from {INVENTORY_SLOT_PATH}")
        return

    # Perform template matching on grayscale images
    result = cv2.matchTemplate(screenshot_gray, inventory_slot_template, cv2.TM_CCOEFF_NORMED)

    # Get the locations of the matches (threshold for matching)
    threshold = 0.8  # Adjust the threshold as necessary
    locations = np.where(result >= threshold)

    # Get the number of matches found
    match_count = len(locations[0])
    print(f"Found {match_count} matches for the inventory slot template.")

    # Apply non-maximum suppression to remove overlapping matches
    boxes = []
    for pt in zip(*locations[::-1]):  # `zip(*locations[::-1])` gives (x, y) coordinates of each match
        x, y = pt
        boxes.append([x + inventory_region[0], y + inventory_region[1], inventory_slot_template.shape[1], inventory_slot_template.shape[0]])

    # Use cv2.dnn.NMSBoxes to suppress redundant bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, np.ones(len(boxes)), 0.8, 0.2)  # Confidence and overlap threshold

    if len(indices) > 0:
        print(f"Found {len(indices)} distinct inventory slots after NMS.")

        # If exactly 27 distinct matches are found, proceed to drop items
        if len(indices.flatten()) == 27:
            print("Inventory is full (exactly 27 items). Dropping items...")

            # Iterate over each match and click to drop the items
            for i in indices.flatten():  # Flatten the indices and iterate over them
                x, y, w, h = boxes[i]
                center = (x + w // 2, y + h // 2)
                print(f"Dropping item at {center}")

                # Focus the game window before clicking
                focus_game_window()
                pyautogui.moveTo(center)  # Move the mouse to the center of the inventory slot
                pyautogui.keyDown('shift')  # Hold down the shift key
                pyautogui.click()  # Left-click to drop the item
                pyautogui.keyUp('shift')  # Release the shift key

                # Add a delay after the click to ensure the drop action is registered
                time.sleep(0.5)  # Increase the delay between drops to allow for better registration

        else:
            print("Inventory is not full (exactly 27 items needed). No items will be dropped.")
    else:
        print("No valid inventory slots found after NMS.")

# Main loop to repeatedly search and click with random delays
def main():
    global tree_region, inventory_region

    print("Tree and Inventory regions are set in the code.")

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

        # Drop items if inventory is full
        drop_items_from_inventory()

if __name__ == "__main__":
    main()
