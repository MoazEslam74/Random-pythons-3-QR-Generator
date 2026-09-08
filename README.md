<p align="center">
  <img src="RP_Certificates_Generator.ico" alt="Centered image" width="300">
</p>
# Advanced QR Code Generator

A feature-rich desktop application built with Python and Tkinter that allows users to generate high-quality QR codes from URLs. The application includes advanced features such as embedding custom logos, link previewing, dual-language support, and smart keyboard shortcut handling.

## ✨ Features

- **Link to QR Code**: Quickly convert any URL or text into a scannable QR code.
- **Link Auto-Preview**: A dedicated "Preview" button allows users to verify the link in their default web browser before generating the QR code.
- **Custom Logo/Icon Support**: Embed your own logo in the center of the QR code (uses High Error Correction to maintain readability).
- **Icon Shape Masking**: Choose how your embedded logo looks with built-in cropping options:
  - Square
  - Rounded Corners
  - Circle
- **Dual Language UI**: Switch seamlessly between English and Arabic interfaces with a single click.
- **Smart Keyboard Shortcuts**: Full support for copy/paste/cut/select-all shortcuts (Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+A), even when using the Arabic keyboard layout.
- **Instant Export**: Automatically saves the generated QR code as `Exported.png` in the project directory.

## 🛠️ Built With

- **Python 3.x**
- **Tkinter**: Standard Python interface to the Tcl/Tk GUI toolkit.
- **[qrcode](https://pypi.org/project/qrcode/)**: For generating the QR code matrix.
- **[Pillow (PIL)](https://pypi.org/project/Pillow/)**: For image processing, resizing, and shape masking (drawing circles, rounded rectangles).
- **webbrowser**: Built-in Python library for the link preview feature.

## 🚀 Installation & Setup

Follow these steps to get the app running on your local machine:

### 1. Prerequisites
Make sure you have Python installed on your system (Python 3.6 or newer is recommended). 

### 2. Install Required Libraries
The app relies on `qrcode` and `Pillow`. You can install them via pip. Open your terminal or command prompt and run:

```bash
pip install qrcode pillow
