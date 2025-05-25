# q to quit
# ESC to skip to next
# Enter to save mask go to next
# - to decrease brush size
# shift+ to increase brush size

# Press and Hold left mouse button to brush

# MOUSE Features:
# WHEEL adjustment for brush size increase/decrease
# Right-click to REDO
# WHEEL/Middle button to save mask and next

import cv2
import os
import numpy as np

# Global variables
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial coordinates
img = None  # Image variable
mask = None  # Mask variable
img_stack = []  # Stack for undo functionality
mask_stack = []  # Stack for undo functionality
brush_size = 10  # Initial brush size

# Mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, img, mask, img_stack, mask_stack, brush_size

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        img_stack.append(img.copy())
        mask_stack.append(mask.copy())

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(img, (x, y), brush_size, (255, 255, 255), -1)
            cv2.circle(mask, (x, y), brush_size, 255, -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img, (x, y), brush_size, (255, 255, 255), -1)
        cv2.circle(mask, (x, y), brush_size, 255, -1)

    elif event == cv2.EVENT_RBUTTONDOWN:
        if img_stack and mask_stack:
            img = img_stack.pop()
            mask = mask_stack.pop()
            cv2.imshow('image', img)

    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            brush_size += 1
        elif flags < 0 and brush_size > 1:
            brush_size -= 1
        print(f'Brush size changed to {brush_size}')

    elif event == cv2.EVENT_MBUTTONDOWN:
        save_and_next_image()

def save_and_next_image():
    global img, mask, images, current_image_idx, output_folder, resized_folder

    image_file = images[current_image_idx]
    mask_file_name = os.path.splitext(image_file)[0] + '.png'
    mask_path = os.path.join(output_folder, mask_file_name)
    resized_file_name = os.path.splitext(image_file)[0] + '.jpg'
    resized_path = os.path.join(resized_folder, resized_file_name)

    # Save the mask with transparency
    mask_rgba = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    mask_rgba[:, :, 3] = mask  # Set alpha channel to mask values
    cv2.imwrite(mask_path, mask_rgba)
    # Save the resized image as jpg
    cv2.imwrite(resized_path, img_org)

    current_image_idx += 1
    if current_image_idx >= len(images):
        print("No more images to process.")
        cv2.destroyAllWindows()
    else:
        load_next_image()

def load_next_image():
    global img, mask, img_stack, mask_stack, img_org, current_image_idx

    if current_image_idx >= len(images):
        print("No more images to process.")
        cv2.destroyAllWindows()
        return

    image_file = images[current_image_idx]
    mask_file_name = os.path.splitext(image_file)[0] + '.png'
    mask_path = os.path.join(output_folder, mask_file_name)

    # Skip if the mask already exists
    if os.path.exists(mask_path):
        print(f"Skipping {image_file} as mask already exists.")
        current_image_idx += 1
        load_next_image()
        return

    img_path = os.path.join(image_folder, image_file)
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))  # Resize to your required input size
    img_org = img.copy()
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)  # Create a mask to draw annotations
    img_stack.clear()
    mask_stack.clear()
    cv2.setWindowTitle('image', f'Creating Mask for: {image_file}')
    cv2.imshow('image', img)

def main(image_folder, output_folder, resized_folder):
    global img, mask, img_stack, mask_stack, brush_size, images, current_image_idx, img_org

    images = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]
    current_image_idx = 0

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 800, 600)  # Set the window to a larger size
    cv2.setMouseCallback('image', draw_circle)

    load_next_image()

    while True:
        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # ESC key to stop
            print("Skipping current image.")
            current_image_idx += 1
            if current_image_idx >= len(images):
                print("No more images to process.")
                break
            else:
                load_next_image()
        elif k == 13:  # Enter key to save and move to the next image
            save_and_next_image()
        elif k == ord('q'):  # 'q' key to quit the program
            print("Quitting the program.")
            cv2.destroyAllWindows()
            return

    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_folder = 'dataset/Source_Image'
    output_folder = 'dataset/Mask'
    resized_folder = 'dataset/Image'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(resized_folder):
        os.makedirs(resized_folder)

    main(image_folder, output_folder, resized_folder)
