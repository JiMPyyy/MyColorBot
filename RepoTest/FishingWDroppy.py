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

# Path to inventory slot reference image (you can create this using a screenshot of a full inventory slot)
INVENTORY_SLOT_PATH = r'C:\Users\potte\OneDrive\Desktop\FullInventory.png'

# Global variables for manually defined regions
# Manually set the (x, y, width, height) for the tree and inventory regions
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

# Function to highlight regions on the screenshot
def highlight_region(screenshot, region, color=(0, 255, 0)):
    """Draw a rectangle around the specified region."""
    x, y, w, h = region
    # Draw a rectangle on the screenshot
    cv2.rectangle(screenshot, (x, y), (x + w, y + h), color, 2)  # Green rectangle with thickness=2
    return screenshot

# Function to check if the inventory is full by using the inventory slot reference image
def is_inventory_full(screenshot, inventory_region):
    # Load the inventory slot reference image
    slot_template = cv2.imread(INVENTORY_SLOT_PATH)

    if slot_template is None:
        print("Error: Inventory slot template image could not be loaded.")
        return False

    # Convert screenshot and template to grayscale for matching
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    slot_template_gray = cv2.cvtColor(slot_template, cv2.COLOR_BGR2GRAY)

    # Define the area of the inventory in the screenshot
    x, y, w, h = inventory_region
    inventory_area = screenshot_gray[y:y+h, x:x+w]

    # Perform template matching to find each inventory slot in the inventory area
    result = cv2.matchTemplate(inventory_area, slot_template_gray, cv2.TM_CCOEFF_NORMED)

    # Define a threshold for matching
    threshold = 0.8  # Adjust this as needed for sensitivity
    locations = np.where(result >= threshold)

    # Check if all inventory slots are filled
    num_matches = len(locations[0])  # How many slots matched the reference image
    expected_num_matches = (w // slot_template.shape[1]) * (h // slot_template.shape[0])  # Total slots in the region

    print(f"Found {num_matches} matches out of {expected_num_matches} expected.")
    
    # If the number of matches equals the expected number, the inventory is full
    return num_matches == expected_num_matches

# Function to drop items from the inventory by Shift + Left Click
def drop_items_from_inventory():
    if inventory_region is None:
        print("Inventory region is not defined.")
        return

    # Take a screenshot of the screen using pyautogui
    screenshot = pyautogui.screenshot()

    # Convert screenshot from RGB (PIL) to BGR (OpenCV format)
    screenshot = np.array(screenshot)  # Convert to NumPy array
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR

    # Check if the inventory is full
    if is_inventory_full(screenshot, inventory_region):
        print("Inventory is full. Dropping items...")

        # Loop through the inventory slots and drop the items
        x, y, w, h = inventory_region
        num_slots_x = w // 32  # Assuming each slot is 32px wide
        num_slots_y = h // 32  # Assuming each slot is 32px high
        
        for row in range(num_slots_y):
            for col in range(num_slots_x):
                # Calculate the center position of each slot
                slot_x = x + col * 32 + 16  # 16px is half the slot width for center
                slot_y = y + row * 32 + 16  # 16px is half the slot height for center

                # Focus the game window before clicking
                focus_game_window()
                time.sleep(0.2)  # Ensure a small delay before interacting with the game
                
                # Move to the slot and perform Shift + Left Click to drop the item
                pyautogui.moveTo(slot_x, slot_y)
                time.sleep(0.2)  # Small delay to simulate a more human-like movement
                pyautogui.keyDown('shift')  # Hold down the 'Shift' key
                pyautogui.click()  # Left click to drop the item
                pyautogui.keyUp('shift')  # Release the 'Shift' key
                
                # Add a short delay after each click to ensure it's registered
                time.sleep(0.5)

                print(f"Dropped item from slot ({col+1},{row+1})")

    else:
        print("Inventory is not full.")

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

        # Check if the inventory is full and drop items if necessary
        drop_items_from_inventory()

        # Randomly sleep between 15 to 30 seconds
        random_delay = random.uniform(10, 20)
        print(f"Waiting for {random_delay:.2f} seconds...")
        time.sleep(random_delay)  # Sleep for a random amount of time between 15 and 30 seconds

if __name__ == "__main__":
    main()
