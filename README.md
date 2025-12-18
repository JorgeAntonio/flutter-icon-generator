# Flutter Icon Generator

This is a Python utility script designed to automatically generate the necessary icons for a Flutter application, specifically tailored for iOS and Android (adaptive icons).

## Description

The script takes an input image (logo) and generates two resized and centered versions:

1.  **`icon-1024x1024.png`**: A master icon of 1024x1024 pixels with a white background. Ideal for the App Store and as a base for generating other sizes on iOS.
2.  **`icon-foreground-432x432.png`**: A foreground icon of 432x432 pixels with a transparent background. Designed to be used as the foreground layer for Android adaptive icons.

The script ensures the aspect ratio of the original logo is maintained and centers it on the canvas, applying safety margins to avoid cropping on devices with circular or rounded icon masks.

## Requirements

*   Python 3.x
*   Python libraries: `Pillow`, `numpy`

## Installation

1.  Ensure you have a virtual environment activated (optional but recommended).
2.  Install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install Pillow numpy
```

## Usage

1.  Place your original image (logo) in the same directory as the `main.py` script.
2.  Make sure the filename matches the `input_path` variable in `main.py` (default: `"LOGO ESCUELA POSTGRADO UNAP SIN LETRA 2.png"`) or edit the script to use your filename.
3.  Run the script:

```bash
python main.py
```

4.  The script will generate the files `icon-1024x1024.png` and `icon-foreground-432x432.png` in the same directory.
5.  Copy these files to the `assets/images/` folder (or the corresponding path) of your Flutter project and run the Flutter icon generation commands (e.g., using `flutter_launcher_icons`).
