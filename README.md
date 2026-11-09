# PDFWorks Studio

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Qt6-orange.svg)](https://pypi.org/project/PySide6/)

A free, fast, and feature-rich native Linux desktop PDF and office document utility suite, built specifically for Linux environments (optimized for CachyOS, Arch Linux, Ubuntu, Fedora, and other modern distributions).

---

## Features

### PDF Utilities
- **Merge PDF**: Combine multiple PDF files into one with visual thumbnail previews and drag/move reordering.
- **Split PDF**: Extract specific pages or split documents into individual single-page files.
- **Compress PDF**: Reduce PDF file size efficiently using PyMuPDF.
- **Images to PDF**: Convert PNG, JPG, or BMP images into a PDF document with live thumbnail previews and reordering.
- **PDF to Images**: Convert PDF pages into high-resolution PNG or JPG images in bulk.
- **Rotate PDF**: Rotate PDF pages by 90°, 180°, or 270°.
- **Protect PDF**: Encrypt documents with secure passwords.
- **Unlock PDF**: Remove password security from protected PDF files.
- **Extract Images**: Extract all embedded images from a PDF file into dedicated subfolders.
- **Watermark PDF**: Apply professional text watermarks across all pages.

### Office Document Conversions
- **Word to PDF** (`.docx` → `.pdf`)
- **PowerPoint to PDF** (`.pptx` → `.pdf`)
- **PDF to Word** (`.pdf` → `.docx`)
- **PDF to PowerPoint** (`.pdf` → `.pptx`)

> **Note on Office Conversion Fidelity**: 
> For 100% native layout fidelity matching Microsoft Office / OnlyOffice printing, the app automatically detects and leverages **LibreOffice** (`libreoffice` / `soffice`) if installed. If LibreOffice is not detected, it automatically falls back to high-fidelity built-in Python rendering (`python-docx` / `python-pptx` + `PyMuPDF`) and suggests the correct package manager command for your distribution (`pacman`, `apt`, `dnf`, `zypper`).

---

## Installation & Usage

Choose one of two convenient ways to use PDFWorks Studio:

### Option A: Download Portable AppImage (Recommended for all Linux distributions)
1. Go to the [Releases](https://github.com/deesspanda/pdfworks-studio/releases) tab.
2. Download `PDFWorks_Studio-x86_64.AppImage`.
3. Make it executable and run:
   ```bash
   chmod +x PDFWorks_Studio-x86_64.AppImage
   ./PDFWorks_Studio-x86_64.AppImage
   ```

### Option B: Clone & Run from Source (For developers & Arch/CachyOS)
1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/deesspanda/pdfworks-studio.git
   cd pdfworks-studio
   ```
2. Set up dependencies and run instantly using the provided run script:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ./run.sh
   ```
   *(Or install natively on Arch / CachyOS via `makepkg -si` using the provided `PKGBUILD`)*

---

## Tech Stack
- **Python 3** with **PySide6 (Qt6)** for native, hardware-accelerated UI with **Material Expressive + Clear Glass** design.
- **PyMuPDF (`pymupdf`)** & **`pypdf`** for high-performance PDF manipulation.
- **`pdf2docx` & `python-pptx`** for Word and PowerPoint conversions.
- **Pillow** for image processing.

---

## License
Distributed under the **MIT License**. See `LICENSE` for more information.
