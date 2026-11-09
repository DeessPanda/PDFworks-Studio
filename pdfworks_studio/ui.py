import os
from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QPainter, QLinearGradient, QRadialGradient, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QFileDialog, QMessageBox,
    QListWidget, QListWidgetItem, QLineEdit, QSpinBox, QComboBox, QDialog, QFormLayout,
    QScrollArea, QFrame, QProgressBar
)
from pdfworks_studio.tools import PDFTools

class ExpressiveGlassBackground(QWidget):
    """Custom widget to draw a Material Expressive background with soft glowing shapes."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Rich Material Expressive base gradient (Indigo to Deep Slate/Violet)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#1e1b4b"))  # Deep Indigo
        gradient.setColorAt(0.5, QColor("#312e81"))  # Rich Violet-Indigo
        gradient.setColorAt(1.0, QColor("#0f172a"))  # Deep Slate
        painter.fillRect(self.rect(), gradient)

        # Draw soft glowing floating organic circles (Material Expressive abstract shapes)
        painter.setPen(Qt.NoPen)

        # Glowing orb 1 (Cyan/Blue)
        grad1 = QRadialGradient(self.width() * 0.2, self.height() * 0.3, 400)
        grad1.setColorAt(0.0, QColor(59, 130, 246, 80))
        grad1.setColorAt(1.0, QColor(59, 130, 246, 0))
        painter.setBrush(grad1)
        painter.drawEllipse(QRectF(-100, -50, 600, 600))

        # Glowing orb 2 (Emerald/Teal)
        grad2 = QRadialGradient(self.width() * 0.8, self.height() * 0.7, 500)
        grad2.setColorAt(0.0, QColor(16, 185, 129, 70))
        grad2.setColorAt(1.0, QColor(16, 185, 129, 0))
        painter.setBrush(grad2)
        painter.drawEllipse(QRectF(self.width() - 400, self.height() - 400, 700, 700))

        # Glowing orb 3 (Purple/Pink accent)
        grad3 = QRadialGradient(self.width() * 0.6, self.height() * 0.2, 350)
        grad3.setColorAt(0.0, QColor(168, 85, 247, 65))
        grad3.setColorAt(1.0, QColor(168, 85, 247, 0))
        painter.setBrush(grad3)
        painter.drawEllipse(QRectF(self.width() * 0.4, -100, 500, 500))


class ToolDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(760, 580)
        self.setMinimumSize(620, 500)

        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', Inter, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #e2e8f0;
                font-weight: 500;
                background: transparent;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border-radius: 10px;
                padding: 10px 16px;
                font-weight: 600;
                font-size: 13px;
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2563eb, stop:1 #1d4ed8);
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 10px 14px;
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 10px;
                background-color: #1e293b;
                font-size: 13px;
                color: #f8fafc;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 2px solid #38bdf8;
                background-color: #0f172a;
            }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: #f8fafc;
                selection-background-color: #3b82f6;
                selection-color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
            }
            QListWidget {
                background-color: #1e293b;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 14px;
                padding: 8px;
                font-size: 13px;
                color: #f8fafc;
            }
            QListWidget::item {
                padding: 8px 10px;
                border-radius: 8px;
                margin-bottom: 4px;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
                color: white;
                font-weight: 600;
            }
            QListWidget::item:hover {
                background-color: rgba(59, 130, 246, 0.3);
            }
            QProgressBar {
                background-color: #1e293b;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                text-align: center;
                color: white;
                font-weight: bold;
                font-size: 12px;
                height: 22px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #10b981);
                border-radius: 7px;
            }
        """)

    @staticmethod
    def generate_thumbnail(path):
        """Generate a small thumbnail QIcon for image or PDF files with clean memory handling."""
        try:
            ext = os.path.splitext(path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']:
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    return QIcon(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            elif ext == '.pdf':
                import pymupdf as fitz
                with fitz.open(path) as doc:
                    if len(doc) > 0:
                        page = doc[0]
                        pix = page.get_pixmap(matrix=fitz.Matrix(0.3, 0.3))
                        qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                        pixmap = QPixmap.fromImage(qimg)
                        if not pixmap.isNull():
                            return QIcon(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception:
            pass
        return QIcon()


class BatchToolDialog(ToolDialog):
    def __init__(self, title, file_filter, parent=None):
        super().__init__(title, parent)
        self.file_filter = file_filter

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        layout.addWidget(QLabel("Select Files (Multiple files supported with live thumbnails):"))
        self.file_list = QListWidget()
        self.file_list.setIconSize(QSize(48, 48))
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Add Files")
        btn_add.clicked.connect(self.add_files)
        btn_remove = QPushButton("Remove Selected")
        btn_remove.clicked.connect(self.remove_files)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_remove)
        layout.addLayout(btn_layout)

        # Output directory selection
        out_layout = QHBoxLayout()
        self.out_dir_edit = QLineEdit()
        self.out_dir_edit.setPlaceholderText("Select output directory (defaults to input dir)...")
        btn_out = QPushButton("Browse...")
        btn_out.clicked.connect(self.browse_out_dir)
        out_layout.addWidget(QLabel("Output Dir:"))
        out_layout.addWidget(self.out_dir_edit)
        out_layout.addWidget(btn_out)
        layout.addLayout(out_layout)

        # Extra options layout
        self.extra_layout = QVBoxLayout()
        layout.addLayout(self.extra_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.btn_run = QPushButton("Process Files")
        self.btn_run.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10b981, stop:1 #059669);
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-weight: 700;
                font-size: 14px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #059669, stop:1 #047857);
            }
        """)
        self.btn_run.clicked.connect(self.run_process_wrapper)
        layout.addWidget(self.btn_run)

    def add_files(self):
        home_dir = os.path.expanduser("~")
        if not os.path.exists(home_dir):
            home_dir = os.getcwd()

        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", home_dir, self.file_filter)
        if files:
            for f in files:
                existing = [self.file_list.item(i).data(Qt.UserRole) for i in range(self.file_list.count())]
                if f not in existing:
                    item = QListWidgetItem(os.path.basename(f))
                    item.setData(Qt.UserRole, f)
                    item.setToolTip(f)
                    icon = self.generate_thumbnail(f)
                    if not icon.isNull():
                        item.setIcon(icon)
                    self.file_list.addItem(item)

            if not self.out_dir_edit.text() and files:
                first_dir = os.path.dirname(files[0])
                self.out_dir_edit.setText(first_dir)

    def remove_files(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def get_files(self):
        return [item.data(Qt.UserRole) or item.text() for i in range(self.file_list.count()) for item in [self.file_list.item(i)]]

    def resolve_output_path(self, out_dir, filename):
        out_path = os.path.join(out_dir, filename)
        if os.path.exists(out_path):
            base, ext = os.path.splitext(filename)
            msg = QMessageBox(self)
            msg.setWindowTitle("File Exists Conflict")
            msg.setText(f"The file '{filename}' already exists in the output directory.")
            msg.setInformativeText("Would you like to replace it or create a duplicate?")
            btn_replace = msg.addButton("Replace", QMessageBox.AcceptRole)
            btn_duplicate = msg.addButton("Create Duplicate", QMessageBox.ActionRole)
            btn_cancel = msg.addButton("Cancel", QMessageBox.RejectRole)
            msg.exec()

            clicked = msg.clickedButton()
            if clicked == btn_replace:
                return out_path, "replace"
            elif clicked == btn_duplicate:
                counter = 1
                while os.path.exists(out_path):
                    out_path = os.path.join(out_dir, f"{base}({counter}){ext}")
                    counter += 1
                return out_path, "duplicate"
            else:
                return None, "cancel"
        return out_path, "new"

    def browse_out_dir(self):
        home_dir = os.path.expanduser("~")
        if not os.path.exists(home_dir):
            home_dir = os.getcwd()
        d = QFileDialog.getExistingDirectory(self, "Select Output Directory", home_dir)
        if d:
            self.out_dir_edit.setText(d)

    def run_process_wrapper(self):
        files = self.get_files()
        out_dir = self.out_dir_edit.text()
        if not files:
            QMessageBox.warning(self, "Warning", "Please select at least one file.")
            return
        if not out_dir or not os.path.exists(out_dir):
            QMessageBox.warning(self, "Warning", "Please select a valid output directory.")
            return

        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.btn_run.setEnabled(False)
        QApplication.processEvents()

        try:
            self.run_process_batch(files, out_dir)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during processing:\n{str(e)}")
        finally:
            self.btn_run.setEnabled(True)

    def run_process_batch(self, files, out_dir):
        pass


class MergeDialog(ToolDialog):
    def __init__(self, parent=None):
        super().__init__("Merge PDFs", parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        layout.addWidget(QLabel("Select PDF files to merge (reorder & preview thumbnails):"))
        self.file_list = QListWidget()
        self.file_list.setIconSize(QSize(48, 48))
        self.file_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Add Files")
        btn_add.clicked.connect(self.add_files)
        btn_remove = QPushButton("Remove")
        btn_remove.clicked.connect(lambda: [self.file_list.takeItem(self.file_list.row(i)) for i in self.file_list.selectedItems()])

        btn_up = QPushButton("Move Up")
        btn_up.clicked.connect(self.move_item_up)
        btn_down = QPushButton("Move Down")
        btn_down.clicked.connect(self.move_item_down)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_remove)
        btn_layout.addWidget(btn_up)
        btn_layout.addWidget(btn_down)
        layout.addLayout(btn_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.btn_run = QPushButton("Merge PDFs")
        self.btn_run.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10b981, stop:1 #059669);
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-weight: 700;
                font-size: 14px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #059669, stop:1 #047857);
            }
        """)
        self.btn_run.clicked.connect(self.run_merge)
        layout.addWidget(self.btn_run)

    def add_files(self):
        home_dir = os.path.expanduser("~")
        if not os.path.exists(home_dir):
            home_dir = os.getcwd()
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", home_dir, "PDF Files (*.pdf)")
        if files:
            for f in files:
                item = QListWidgetItem(os.path.basename(f))
                item.setData(Qt.UserRole, f)
                item.setToolTip(f)
                icon = self.generate_thumbnail(f)
                if not icon.isNull():
                    item.setIcon(icon)
                self.file_list.addItem(item)

    def move_item_up(self):
        row = self.file_list.currentRow()
        if row > 0:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row - 1, item)
            self.file_list.setCurrentRow(row - 1)

    def move_item_down(self):
        row = self.file_list.currentRow()
        if row >= 0 and row < self.file_list.count() - 1:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row + 1, item)
            self.file_list.setCurrentRow(row + 1)

    def run_merge(self):
        if self.file_list.count() < 2:
            QMessageBox.warning(self, "Warning", "Please select at least 2 PDF files to merge.")
            return

        home_dir = os.path.expanduser("~")
        if self.file_list.count() > 0:
            home_dir = os.path.dirname(self.file_list.item(0).data(Qt.UserRole) or self.file_list.item(0).text())

        out, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", os.path.join(home_dir, "merged.pdf"), "PDF Files (*.pdf)")
        if out:
            self.progress_bar.show()
            self.progress_bar.setValue(50)
            self.btn_run.setEnabled(False)
            QApplication.processEvents()
            try:
                paths = [self.file_list.item(i).data(Qt.UserRole) or self.file_list.item(i).text() for i in range(self.file_list.count())]
                PDFTools.merge_pdfs(paths, out)
                self.progress_bar.setValue(100)
                QMessageBox.information(self, "Success", f"PDFs successfully merged into:\n{out}")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to merge PDFs:\n{str(e)}")
            finally:
                self.btn_run.setEnabled(True)


class SplitDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("Split PDF", "PDF Files (*.pdf)", parent)

        form = QFormLayout()
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Extract all pages as separate files", "Extract specific pages/range"])
        self.mode_combo.currentIndexChanged.connect(self.mode_changed)

        self.spec_edit = QLineEdit()
        self.spec_edit.setPlaceholderText("e.g. 1-3,5,8-10")
        self.spec_label = QLabel("Pages Spec:")

        form.addRow(QLabel("Split Mode:"), self.mode_combo)
        form.addRow(self.spec_label, self.spec_edit)
        self.extra_layout.addLayout(form)

        self.spec_label.hide()
        self.spec_edit.hide()

    def run_process_batch(self, files, out_dir):
        mode = "all" if self.mode_combo.currentIndex() == 0 else "range"
        spec = self.spec_edit.text()
        total_files = len(files)
        total_created = 0
        for i, f in enumerate(files):
            base_name = os.path.splitext(os.path.basename(f))[0]
            sub_dir = os.path.join(out_dir, base_name + "_split")
            res = PDFTools.split_pdf(f, sub_dir, mode=mode, pages_spec=spec)
            total_created += len(res)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Split completed successfully! Created {total_created} file(s) across {total_files} document(s).")
        self.accept()

    def mode_changed(self, idx):
        if idx == 1:
            self.spec_label.show()
            self.spec_edit.show()
        else:
            self.spec_label.hide()
            self.spec_edit.hide()


class CompressDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("Compress PDF", "PDF Files (*.pdf)", parent)

    def run_process_batch(self, files, out_dir):
        total_files = len(files)
        for i, f in enumerate(files):
            filename = os.path.basename(f)
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.compress_pdf(f, out_path)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully processed {total_files} PDF(s) with original names!")
        self.accept()


class ImagesToPdfDialog(ToolDialog):
    def __init__(self, parent=None):
        super().__init__("Images to PDF", parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        layout.addWidget(QLabel("Select Images (PNG/JPG) (reorder & preview thumbnails):"))
        self.file_list = QListWidget()
        self.file_list.setIconSize(QSize(48, 48))
        self.file_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Add Images")
        btn_add.clicked.connect(self.add_images)
        btn_remove = QPushButton("Remove")
        btn_remove.clicked.connect(lambda: [self.file_list.takeItem(self.file_list.row(i)) for i in self.file_list.selectedItems()])

        btn_up = QPushButton("Move Up")
        btn_up.clicked.connect(self.move_item_up)
        btn_down = QPushButton("Move Down")
        btn_down.clicked.connect(self.move_item_down)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_remove)
        btn_layout.addWidget(btn_up)
        btn_layout.addWidget(btn_down)
        layout.addLayout(btn_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        btn_run = QPushButton("Convert to PDF")
        btn_run.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10b981, stop:1 #059669);
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-weight: 700;
                font-size: 14px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #059669, stop:1 #047857);
            }
        """)
        btn_run.clicked.connect(self.run_conversion)
        self.btn_run = btn_run
        layout.addWidget(btn_run)

    def add_images(self):
        home_dir = os.path.expanduser("~")
        if not os.path.exists(home_dir):
            home_dir = os.getcwd()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", home_dir, "Images (*.png *.jpg *.jpeg *.bmp)")
        if files:
            for f in files:
                item = QListWidgetItem(os.path.basename(f))
                item.setData(Qt.UserRole, f)
                item.setToolTip(f)
                icon = self.generate_thumbnail(f)
                if not icon.isNull():
                    item.setIcon(icon)
                self.file_list.addItem(item)

    def move_item_up(self):
        row = self.file_list.currentRow()
        if row > 0:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row - 1, item)
            self.file_list.setCurrentRow(row - 1)

    def move_item_down(self):
        row = self.file_list.currentRow()
        if row >= 0 and row < self.file_list.count() - 1:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row + 1, item)
            self.file_list.setCurrentRow(row + 1)

    def run_conversion(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "Warning", "Please select at least one image.")
            return

        home_dir = os.path.expanduser("~")
        if self.file_list.count() > 0:
            home_dir = os.path.dirname(self.file_list.item(0).data(Qt.UserRole) or self.file_list.item(0).text())

        out, _ = QFileDialog.getSaveFileName(self, "Save PDF", os.path.join(home_dir, "document.pdf"), "PDF Files (*.pdf)")
        if out:
            self.progress_bar.show()
            self.progress_bar.setValue(50)
            self.btn_run.setEnabled(False)
            QApplication.processEvents()
            try:
                paths = [self.file_list.item(i).data(Qt.UserRole) or self.file_list.item(i).text() for i in range(self.file_list.count())]
                PDFTools.images_to_pdf(paths, out)
                self.progress_bar.setValue(100)
                QMessageBox.information(self, "Success", f"Images successfully converted to PDF:\n{out}")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to convert images:\n{str(e)}")
            finally:
                self.btn_run.setEnabled(True)


class PdfToImagesDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("PDF to Images", "PDF Files (*.pdf)", parent)

        form = QFormLayout()
        self.fmt_combo = QComboBox()
        self.fmt_combo.addItems(["png", "jpg"])
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 300)
        self.dpi_spin.setValue(150)

        form.addRow(QLabel("Image Format:"), self.fmt_combo)
        form.addRow(QLabel("DPI (Resolution):"), self.dpi_spin)
        self.extra_layout.addLayout(form)

    def run_process_batch(self, files, out_dir):
        fmt = self.fmt_combo.currentText()
        dpi = self.dpi_spin.value()
        total_files = len(files)
        for i, f in enumerate(files):
            base_name = os.path.splitext(os.path.basename(f))[0]
            sub_dir = os.path.join(out_dir, base_name + "_images")
            PDFTools.pdf_to_images(f, sub_dir, fmt=fmt, dpi=dpi)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully converted {total_files} PDF(s) to images!")
        self.accept()


class RotateDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("Rotate PDF", "PDF Files (*.pdf)", parent)

        form = QFormLayout()
        self.angle_combo = QComboBox()
        self.angle_combo.addItems(["90° Clockwise", "180°", "270° Clockwise (90° Counter-clockwise)"])
        form.addRow(QLabel("Rotation Angle:"), self.angle_combo)
        self.extra_layout.addLayout(form)

    def run_process_batch(self, files, out_dir):
        idx = self.angle_combo.currentIndex()
        angle = 90 if idx == 0 else (180 if idx == 1 else 270)
        total_files = len(files)
        for i, f in enumerate(files):
            filename = os.path.basename(f)
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.rotate_pdf(f, out_path, angle)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully rotated {total_files} PDF(s) retaining original names!")
        self.accept()


class ProtectDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("Protect PDF", "PDF Files (*.pdf)", parent)

        form = QFormLayout()
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        form.addRow(QLabel("Password:"), self.pwd_edit)
        self.extra_layout.addLayout(form)

    def run_process_batch(self, files, out_dir):
        pwd = self.pwd_edit.text()
        if not pwd:
            QMessageBox.warning(self, "Warning", "Please enter a password.")
            return
        total_files = len(files)
        for i, f in enumerate(files):
            filename = os.path.basename(f)
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.protect_pdf(f, out_path, pwd)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully protected {total_files} PDF(s) retaining original names!")
        self.accept()


class UnlockDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("Unlock PDF", "PDF Files (*.pdf)", parent)

        form = QFormLayout()
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        form.addRow(QLabel("Password:"), self.pwd_edit)
        self.extra_layout.addLayout(form)

    def run_process_batch(self, files, out_dir):
        pwd = self.pwd_edit.text()
        if not pwd:
            QMessageBox.warning(self, "Warning", "Please enter the password.")
            return
        total_files = len(files)
        for i, f in enumerate(files):
            filename = os.path.basename(f)
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.unlock_pdf(f, out_path, pwd)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully unlocked {total_files} PDF(s) retaining original names!")
        self.accept()


class ExtractImagesDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("Extract Images from PDF", "PDF Files (*.pdf)", parent)

    def run_process_batch(self, files, out_dir):
        total_files = len(files)
        total_extracted = 0
        for i, f in enumerate(files):
            base_name = os.path.splitext(os.path.basename(f))[0]
            sub_dir = os.path.join(out_dir, base_name + "_images")
            res = PDFTools.extract_images(f, sub_dir)
            total_extracted += len(res)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully extracted {total_extracted} image(s) from {total_files} PDF(s) into subfolders!")
        self.accept()


class WatermarkDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("Watermark PDF", "PDF Files (*.pdf)", parent)

        form = QFormLayout()
        self.text_edit = QLineEdit()
        self.text_edit.setText("CONFIDENTIAL")
        form.addRow(QLabel("Watermark Text:"), self.text_edit)
        self.extra_layout.addLayout(form)

    def run_process_batch(self, files, out_dir):
        text = self.text_edit.text()
        total_files = len(files)
        for i, f in enumerate(files):
            filename = os.path.basename(f)
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.watermark_pdf(f, out_path, text)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully watermarked {total_files} PDF(s) retaining original names!")
        self.accept()


class DocxToPdfDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("Word to PDF", "Word Files (*.docx)", parent)
        if not PDFTools.has_libreoffice():
            cmd = PDFTools.get_install_command()
            QMessageBox.information(
                self,
                "LibreOffice Notice",
                "Works best with LibreOffice for 100% native layout fidelity.\n\n"
                "LibreOffice is not currently detected, so built-in Python fallback conversion will be used.\n\n"
                f"To install LibreOffice on your system:\n{cmd}"
            )

    def run_process_batch(self, files, out_dir):
        total_files = len(files)
        for i, f in enumerate(files):
            base_name = os.path.splitext(os.path.basename(f))[0]
            filename = base_name + ".pdf"
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.docx_to_pdf(f, out_path)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully converted {total_files} Word document(s) to PDF with original names!")
        self.accept()


class PptxToPdfDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("PowerPoint to PDF", "PowerPoint Files (*.pptx)", parent)
        if not PDFTools.has_libreoffice():
            cmd = PDFTools.get_install_command()
            QMessageBox.information(
                self,
                "LibreOffice Notice",
                "Works best with LibreOffice for 100% native layout fidelity.\n\n"
                "LibreOffice is not currently detected, so built-in Python fallback conversion will be used.\n\n"
                f"To install LibreOffice on your system:\n{cmd}"
            )

    def run_process_batch(self, files, out_dir):
        total_files = len(files)
        for i, f in enumerate(files):
            base_name = os.path.splitext(os.path.basename(f))[0]
            filename = base_name + ".pdf"
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.pptx_to_pdf(f, out_path)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully converted {total_files} PowerPoint presentation(s) to PDF with original names!")
        self.accept()


class PdfToDocxDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("PDF to Word", "PDF Files (*.pdf)", parent)

    def run_process_batch(self, files, out_dir):
        total_files = len(files)
        for i, f in enumerate(files):
            base_name = os.path.splitext(os.path.basename(f))[0]
            filename = base_name + ".docx"
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.pdf_to_docx(f, out_path)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully converted {total_files} PDF(s) to Word with original names!")
        self.accept()


class PdfToPptxDialog(BatchToolDialog):
    def __init__(self, parent=None):
        super().__init__("PDF to PowerPoint", "PDF Files (*.pdf)", parent)

    def run_process_batch(self, files, out_dir):
        total_files = len(files)
        for i, f in enumerate(files):
            base_name = os.path.splitext(os.path.basename(f))[0]
            filename = base_name + ".pptx"
            out_path, action = self.resolve_output_path(out_dir, filename)
            if action == "cancel":
                continue
            PDFTools.pdf_to_pptx(f, out_path)
            self.progress_bar.setValue(int(((i + 1) / total_files) * 100))
            QApplication.processEvents()

        QMessageBox.information(self, "Success", f"Successfully converted {total_files} PDF(s) to PowerPoint with original names!")
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFWorks Studio")
        self.resize(1150, 780)
        self.setMinimumSize(850, 620)

        self.bg_widget = ExpressiveGlassBackground(self)
        self.setCentralWidget(self.bg_widget)

        main_layout = QVBoxLayout(self.bg_widget)
        main_layout.setContentsMargins(35, 35, 35, 35)
        main_layout.setSpacing(20)

        # Header
        header_layout = QVBoxLayout()
        title = QLabel("PDFWorks Studio")
        title.setObjectName("Title")
        subtitle = QLabel("Free, fast, and secure batch PDF & Office document tools for Linux")
        subtitle.setObjectName("Subtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # Scroll area for grid of tools
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(24)

        tools_data = [
            ("Merge PDF", "Combine multiple PDF files into one in your preferred order.", MergeDialog),
            ("Split PDF", "Extract specific pages or split a PDF into separate files.", SplitDialog),
            ("Compress PDF", "Reduce PDF file size efficiently.", CompressDialog),
            ("Images to PDF", "Convert JPG, PNG, or BMP images into a PDF document.", ImagesToPdfDialog),
            ("PDF to Images", "Extract every page of a PDF as high-resolution PNG or JPG images.", PdfToImagesDialog),
            ("Rotate PDF", "Rotate PDF pages by 90, 180, or 270 degrees.", RotateDialog),
            ("Protect PDF", "Encrypt your PDF with a secure password.", ProtectDialog),
            ("Unlock PDF", "Remove password security from protected PDF files.", UnlockDialog),
            ("Extract Images", "Extract all embedded images from a PDF file.", ExtractImagesDialog),
            ("Watermark PDF", "Add custom text watermarks across all pages.", WatermarkDialog),
            ("Word to PDF", "Convert Word (.docx) documents to PDF format in batch.", DocxToPdfDialog),
            ("PowerPoint to PDF", "Convert PowerPoint (.pptx) presentations to PDF format in batch.", PptxToPdfDialog),
            ("PDF to Word", "Convert PDF documents to editable Word (.docx) files in batch.", PdfToDocxDialog),
            ("PDF to PowerPoint", "Convert PDF pages into PowerPoint (.pptx) presentations in batch.", PdfToPptxDialog),
        ]

        row, col = 0, 0
        for name, desc, dialog_class in tools_data:
            card = self.create_card(name, desc, dialog_class)
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        self.setStyleSheet("""
            QLabel#Title {
                font-size: 28px;
                font-weight: 800;
                color: #ffffff;
                letter-spacing: 0.5px;
            }
            QLabel#Subtitle {
                font-size: 15px;
                color: #cbd5e1;
                font-weight: 500;
            }
            QFrame#Card {
                background-color: rgba(30, 41, 59, 0.78);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
            QFrame#Card:hover {
                background-color: rgba(30, 41, 59, 0.92);
                border: 2px solid #38bdf8;
            }
            QPushButton#CardButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton#CardButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)

    def create_card(self, title, description, dialog_class):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        layout_title = QLabel(title)
        layout_title.setStyleSheet("font-size: 19px; font-weight: 700; color: #f8fafc; background: transparent;")

        lbl_desc = QLabel(description)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("font-size: 13px; color: #cbd5e1; background: transparent; line-height: 1.4;")

        btn = QPushButton("Open Tool")
        btn.setObjectName("CardButton")
        btn.clicked.connect(lambda: dialog_class(self).exec())

        layout.addWidget(layout_title)
        layout.addWidget(lbl_desc)
        layout.addStretch()
        layout.addWidget(btn)

        return card
