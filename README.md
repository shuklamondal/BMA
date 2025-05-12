# Binary Mask Annotator

An interactive tool using OpenCV for creating binary segmentation masks by freehand drawing with the mouse.

## Features

- Brush drawing with adjustable size
- Undo/Redo with right-click
- Mouse wheel for brush resizing
- Save mask + next image with Enter or mouse middle-click
- Skip to next image with ESC
- Automatically resizes images to 224x224
- Saves binary masks in PNG with alpha channel

## Hotkeys and Controls

| Action                    | Control                        |
|--------------------------|--------------------------------|
| Draw                     | Hold left mouse button         |
| Increase Brush Size      | Mouse Wheel Up / `Shift +`     |
| Decrease Brush Size      | Mouse Wheel Down / `-`         |
| Undo                     | Right-click                    |
| Save & Next              | `Enter` or Middle Mouse Button |
| Skip                     | `ESC`                          |
| Quit                     | `q`                            |

## Directory Structure

```text
image-mask-annotator/
├── annotator.py           # Main annotation script
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── dataset/
    ├── Source_Image/      # Input images (jpg/png)
    ├── Mask/              # Output binary masks (PNG with alpha)
    └── Image/             # Resized annotated images (JPG)

## Installation

```bash
git clone https://github.com/shuklamondal/BMA.git
cd binary-mask-annotator
pip install -r requirements.txt
