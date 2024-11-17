import pyautogui
import time

# Path to the image file you want to search for on the screen
IMAGE_PATH = r'C:\Users\potte\OneDrive\pictures\MyCodePictureTestPNG.PNG'  # Replace with your image file path

# Define the region of the screen to search (optional)
# You can define a region to search within if you don't want to search the entire screen
# SEARCH_AREA = (x, y, width, height) - Specify a rectangle area in the form of a tuple
SEARCH_AREA = None  # Search the entire screen if None

# Function to locate the image on the screen and click it
def find_and_click_image(image_path, region=None):
    try:
        # Locate the image on the screen
        location = pyautogui.locateOnScreen(image_path, region=region)
        
        if location:
            # Get the center of the image (where we will click)
            center = pyautogui.center(location)
            print(f"Image found at {center}, clicking...")
            pyautogui.click(center)  # Click the center of the located image
        else:
            print("Image not found on the screen.")
    except pyautogui.ImageNotFoundException:
        print("Error: Image not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main loop (change the timing as needed)
def main():
    while True:
        find_and_click_image(IMAGE_PATH, SEARCH_AREA)
        time.sleep(1)  # Wait for a second before repeating

if __name__ == "__main__":
    main()
