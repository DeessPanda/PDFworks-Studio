#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

APPDIR="AppDir"
echo "Cleaning previous AppDir..."
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps"

echo "Copying application package..."
cp -r pdfworks_studio "$APPDIR/usr/bin/"

echo "Copying virtual environment..."
cp -r venv "$APPDIR/usr/venv"

echo "Generating AppRun launcher..."
cat << 'EOF' > "$APPDIR/AppRun"
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="$HERE/usr/venv/bin:$PATH"
export PYTHONPATH="$HERE/usr/bin"
exec python3 -m pdfworks_studio.main "$@"
EOF
chmod +x "$APPDIR/AppRun"

echo "Creating desktop entry and icon..."
cat << 'EOF' > "$APPDIR/pdfworks-studio.desktop"
[Desktop Entry]
Type=Application
Name=PDFWorks Studio
Comment=Free, fast, and secure batch PDF & Office document tools for Linux
Exec=pdfworks-studio
Icon=pdfworks-studio
Categories=Office;Utility;
Terminal=false
EOF
cp "$APPDIR/pdfworks-studio.desktop" "$APPDIR/usr/share/applications/"

# Generate clean app icon using Python Pillow
"$PROJECT_DIR/venv/bin/python" -c "
from PIL import Image, ImageDraw
img = Image.new('RGB', (256, 256), color='#1e1b4b')
d = ImageDraw.Draw(img)
d.rectangle([24, 24, 232, 232], fill='#3b82f6', outline='#38bdf8', width=8)
d.text((55, 110), 'PDFWorks', fill='white')
img.save('$APPDIR/pdfworks-studio.png')
"

cp "$APPDIR/pdfworks-studio.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/"
cp "$APPDIR/pdfworks-studio.png" "$APPDIR/.DirIcon"

if command -v appimagetool &> /dev/null; then
    echo "Building AppImage..."
    ARCH=x86_64 appimagetool "$APPDIR" PDFWorks_Studio-x86_64.AppImage
    echo "SUCCESS! AppImage created at: $PROJECT_DIR/PDFWorks_Studio-x86_64.AppImage"
else
    echo "AppDir created successfully at $APPDIR!"
    echo "Please install appimagetool (e.g. yay -S appimagetool) then run: appimagetool AppDir PDFWorks_Studio-x86_64.AppImage"
fi
