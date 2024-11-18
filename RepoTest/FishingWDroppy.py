import cv2
import numpy as np
import pyautogui
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

# Global variables for dynamically selected regions
tree_region = None
inventory_region = None

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

# Function to allow user to select a region dynamically
def select_region(title="Select Region"):
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    # Allow user to select the region
    roi = cv2.selectROI(title, screenshot)  # This will open a window for the user to select the ROI
    cv2.destroyAllWindows()  # Close the OpenCV window after selection
    
    # Debugging: Display the selected region to verify alignment
    x, y, w, h = roi
    cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow(f"Selected Region - {title}", screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return roi  # Returns the (x, y, width, height) of the selected region

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
        center = (best_match[0] + tree_region[0] + template.shape[1] // 2, best_match[1] + tree_region[1] + template.shape[0] // 2)
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

# Function to check if the inventory is full
def check_inventory_full():
    if inventory_region is None:
        print("Inventory region is not defined.")
        return False

    # Take a screenshot of the screen using pyautogui
    screenshot = pyautogui.screenshot()

    # Convert screenshot from RGB (PIL) to BGR (OpenCV format)
    screenshot = np.array(screenshot)  # Convert to NumPy array
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR

    # Crop the image to the selected inventory region
    inventory_screenshot = screenshot[inventory_region[1]:inventory_region[1] + inventory_region[3], inventory_region[0]:inventory_region[0] + inventory_region[2]]

    # Load the inventory slot template image
    inventory_slot = cv2.imread(INVENTORY_SLOT_PATH)

    if inventory_slot is None:
        print(f"Error: Inventory slot image could not be loaded from {INVENTORY_SLOT_PATH}")
        return False

    # Convert both the screenshot region and the inventory slot template to grayscale
    inventory_region_gray = cv2.cvtColor(inventory_screenshot, cv2.COLOR_BGR2GRAY)
    inventory_slot_gray = cv2.cvtColor(inventory_slot, cv2.COLOR_BGR2GRAY)

    # Perform template matching to find the inventory slots
    result = cv2.matchTemplate(inventory_region_gray, inventory_slot_gray, cv2.TM_CCOEFF_NORMED)

    # Get the locations of the matches
    threshold = 0.9  # High confidence threshold for a match
    locations = np.where(result >= threshold)

    # Check if the number of matches is equal to the number of inventory slots
    if len(locations[0]) == 27:  # Adjust this number based on your inventory size (e.g., 28 slots in OSRS)
        print("Inventory is full!")
        return True
    else:
        print("Inventory is not full yet.")
        return False

# Function to drop all items in the inventory
def drop_inventory_items():
    # Load the inventory slot image to get its width and height
    inventory_slot = cv2.imread(INVENTORY_SLOT_PATH)
    if inventory_slot is None:
        print("Error: Inventory slot image could not be loaded.")
        return
    
    slot_width, slot_height = inventory_slot.shape[1], inventory_slot.shape[0]

    # Loop over each slot in the inventory and drop the item
    for i in range(27):  # Assuming 28 slots (adjust if needed)
        # Calculate the (x, y) position for the center of each inventory slot
        # Ensure that the x and y offsets correspond to how your inventory grid is positioned
        x = inventory_region[0] + (i % 7) * slot_width  # Assuming 7 columns
        y = inventory_region[1] + (i // 7) * slot_height  # Assuming 4 rows
        
        # Debugging: draw a circle or rectangle around each calculated position
        pyautogui.moveTo(x, y)
        pyautogui.click()  # Click the slot first to verify the position
        print(f"Clicked slot {i + 1} at ({x}, {y})")

        # Focus the game window before clicking
        focus_game_window()

        # Move to the slot and hold shift, then click
        pyautogui.moveTo(x, y, duration=0.2)  # Move smoothly to the slot (adjust duration as needed)
        pyautogui.keyDown('shift')  # Press down Shift key
        pyautogui.click()  # Click the inventory slot to drop the item
        pyautogui.keyUp('shift')  # Release the Shift key
        print(f"Dropped item in slot {i + 1}")

        # Wait a moment before proceeding to the next slot to ensure the action is registered
        time.sleep(1)  # Increased delay to ensure the shift-click is properly registered

# Main loop to repeatedly search and click with random delays
def main():
    global tree_region, inventory_region

    # Select the region for the tree and inventory dynamically
    print("Select the tree region (draw a box around the tree on the screen):")
    tree_region = select_region("Select Tree Region")

    print("Select the inventory region (draw a box around the inventory on the screen):")
    inventory_region = select_region("Select Inventory Region")
    
    while True:
        # Check if the 'Q' key is pressed, if so, break the loop and stop the script
        if keyboard.is_pressed('q'):  # 'q' to quit
            print("Exiting the script...")
            break
        
        find_and_click_tree()  # Perform the image search and click

        # Check if the inventory is full
        if check_inventory_full():
            print("Inventory is full. Dropping items...")
            drop_inventory_items()  # Drop the items

        # Randomly sleep between 15 to 30 seconds
        random_delay = random.uniform(10, 20)
        print(f"Waiting for {random_delay:.2f} seconds...")
        time.sleep(random_delay)  # Sleep for a random amount of time between 15 and 30 seconds

if __name__ == "__main__":
    main()
