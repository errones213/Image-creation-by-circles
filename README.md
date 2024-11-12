
# Image Creation by Circles

This project creates an animation where circles simulate pixels to form an image in three phases: **floating**, **alignment**, and **falling**. The effect is created using Python libraries, including `pymunk` for physics and `matplotlib` for visualization.

## Features
- **Image to Circle Animation**: Converts an image into animated circles.
- **Three-phase Animation**: Floating, formation, and falling phases.
- **Simple Customization**: Replace the image file to use your own pictures.

## Prerequisites
- **Python 3.7+**
- Libraries:
  - `numpy`
  - `matplotlib`
  - `pymunk`
  - `Pillow`

## Getting Started

1. **Clone** this repository:
   ```bash
   git clone https://github.com/errones213/Image-creation-by-circles.git
   ```
2. **Navigate** to the project folder:
   ```bash
   cd Image-creation-by-circles
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add an Image**:
   - Place an image file named `Example_Image.png` in the project folder. 
   - Alternatively, edit the `image_path` variable in `main.py` to point to a different image file.

## Usage

Run the project with:
```bash
python main.py
```

This will start the animation, which will also save as a video file named `video.mp4` if `save = True` is set in the code.

---

## Installing Python and Visual Studio Code (Beginner Guide)

If you're new to Python and Visual Studio Code, follow these steps:

### Step 1: Install Python
1. [Download Python](https://www.python.org/downloads/).
2. Run the installer and check **"Add Python to PATH"** before clicking "Install Now."
3. Confirm the installation in your terminal:
   ```bash
   python --version
   ```

### Step 2: Install Visual Studio Code
1. [Download VS Code](https://code.visualstudio.com/).
2. Run the installer and open VS Code.
3. Go to the **Extensions** view (`Ctrl+Shift+X`) and install the **Python extension** by Microsoft.

### Step 3: Run the Project in VS Code
1. Open the project folder in VS Code (`File > Open Folder`).
2. Open a terminal (`Terminal > New Terminal`).
3. Run:
   ```bash
   python main.py
   ```

---

## Credits
This project uses open-source libraries like `pymunk` for physics and `matplotlib` for animations. Special thanks to these projects for enabling rich, animated visualizations.
