import cv2
import numpy as np
import pyautogui
import time

time.sleep(3)
# Variables to store the starting point of the drag and the current mouse position
start_x, start_y = -1, -1
end_x, end_y = -1, -1

# This function will handle mouse events for dragging
def mouse_callback(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y
    
    # When the left mouse button is pressed, store the start point
    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y  # Start of drag
        print(f"Starting drag at: ({start_x}, {start_y})")
    
    # When the left mouse button is released, finalize the drag and print coordinates
    elif event == cv2.EVENT_LBUTTONUP:
        end_x, end_y = x, y  # End of drag
        print(f"Dragging finished at: ({end_x}, {end_y})")
        
        # Draw the rectangle on the image
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        cv2.imshow("Drag to select area", image)

# Capture the screen once
def capture_screen():
    global image
    
    # Take a screenshot using pyautogui (this will capture the current screen)
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a NumPy array (which OpenCV can work with)
    image = np.array(screenshot)
    
    # Convert the image from RGB (PIL format) to BGR (OpenCV format)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Display the screenshot in an OpenCV window
    cv2.imshow("Drag to select area", image)

    # Set up mouse callback to track dragging and drawing the rectangle
    cv2.setMouseCallback("Drag to select area", mouse_callback)

    # Wait until the user presses 'q' to quit
    while True:
        # If the 'q' key is pressed, break the loop and exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Close the window once we're done
    cv2.destroyAllWindows()

# Main function to start the process
if __name__ == "__main__":
    capture_screen()
