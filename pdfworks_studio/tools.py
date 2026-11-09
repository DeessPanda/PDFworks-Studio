import os
import subprocess
from pypdf import PdfReader, PdfWriter
import pymupdf as fitz  # PyMuPDF
from PIL import Image
from pdf2docx import Converter
from pptx import Presentation
from pptx.util import Inches
from docx import Document

class PDFTools:
    @staticmethod
    def has_libreoffice():
        for cmd in ["libreoffice", "soffice"]:
            if subprocess.run(["which", cmd], capture_output=True).returncode == 0:
                return True
        return False

    @staticmethod
    def get_install_command():
        try:
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release", "r") as f:
                    content = f.read().lower()
                if "arch" in content or "cachyos" in content or "manjaro" in content:
                    return "sudo pacman -S libreoffice-fresh"
                elif "debian" in content or "ubuntu" in content or "mint" in content:
                    return "sudo apt install libreoffice"
                elif "fedora" in content or "rhel" in content or "centos" in content:
                    return "sudo dnf install libreoffice"
                elif "suse" in content:
                    return "sudo zypper install libreoffice"
        except Exception:
            pass
        return "sudo pacman -S libreoffice-fresh (or your system package manager)"

    @staticmethod
    def merge_pdfs(input_paths, output_path):
        writer = PdfWriter()
        for path in input_paths:
            writer.append(path)
        with open(output_path, "wb") as f:
            writer.write(f)
        writer.close()
        return output_path

    @staticmethod
    def split_pdf(input_path, output_dir, mode="all", pages_spec=""):
        reader = PdfReader(input_path)
        os.makedirs(output_dir, exist_ok=True)
        output_files = []

        if mode == "all":
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                out_path = os.path.join(output_dir, f"page_{i+1}.pdf")
                with open(out_path, "wb") as f:
                    writer.write(f)
                output_files.append(out_path)
        elif mode == "range":
            ranges = pages_spec.split(",")
            writer = PdfWriter()
            for r in ranges:
                if "-" in r:
                    start, end = map(int, r.split("-"))
                    for p in range(start - 1, min(end, len(reader.pages))):
                        writer.add_page(reader.pages[p])
                else:
                    p = int(r) - 1
                    if 0 <= p < len(reader.pages):
                        writer.add_page(reader.pages[p])
            out_path = os.path.join(output_dir, "extracted_pages.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            output_files.append(out_path)
        return output_files

    @staticmethod
    def compress_pdf(input_path, output_path):
        doc = fitz.open(input_path)
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()
        return output_path

    @staticmethod
    def images_to_pdf(image_paths, output_path):
        images = []
        for img_path in image_paths:
            img = Image.open(img_path)
            if img.mode != "RGB":
                img = img.convert("RGB")
            images.append(img)
        if images:
            images[0].save(output_path, save_all=True, append_images=images[1:])
        return output_path

    @staticmethod
    def pdf_to_images(input_path, output_dir, fmt="png", dpi=150):
        doc = fitz.open(input_path)
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=matrix)
            out_path = os.path.join(output_dir, f"page_{i+1}.{fmt}")
            pix.save(out_path)
            output_files.append(out_path)
        doc.close()
        return output_files

    @staticmethod
    def rotate_pdf(input_path, output_path, rotation_angle):
        reader = PdfReader(input_path)
        writer = PdfWriter()
        for page in reader.pages:
            page.rotate(rotation_angle)
            writer.add_page(page)
        with open(output_path, "wb") as f:
            writer.write(f)
        return output_path

    @staticmethod
    def protect_pdf(input_path, output_path, user_password, owner_password=""):
        reader = PdfReader(input_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(user_password=user_password, owner_password=owner_password or user_password)
        with open(output_path, "wb") as f:
            writer.write(f)
        return output_path

    @staticmethod
    def unlock_pdf(input_path, output_path, password):
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            reader.decrypt(password)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open(output_path, "wb") as f:
            writer.write(f)
        return output_path

    @staticmethod
    def extract_images(input_path, output_dir):
        doc = fitz.open(input_path)
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        for i, page in enumerate(doc):
            for img_index, img in enumerate(page.get_images(full=True)):
                base_image = doc.extract_image(img[0])
                image_name = os.path.join(output_dir, f"image_p{i+1}_{img_index+1}.{base_image['ext']}")
                with open(image_name, "wb") as f:
                    f.write(base_image["image"])
                output_files.append(image_name)
        doc.close()
        return output_files

    @staticmethod
    def watermark_pdf(input_path, output_path, watermark_text):
        doc = fitz.open(input_path)
        for page in doc:
            rect = page.rect
            point = fitz.Point(rect.width / 2 - 100, rect.height / 2)
            page.insert_text(point, watermark_text, fontsize=36, color=(0.7, 0.7, 0.7), rotate=0)
        doc.save(output_path)
        doc.close()
        return output_path

    @staticmethod
    def docx_to_pdf(input_path, output_path):
        if PDFTools.has_libreoffice():
            for cmd in ["libreoffice", "soffice"]:
                if subprocess.run(["which", cmd], capture_output=True).returncode == 0:
                    out_dir = os.path.dirname(output_path)
                    subprocess.run([cmd, "--headless", "--convert-to", "pdf", input_path, "--outdir", out_dir], check=True)
                    base_name = os.path.splitext(os.path.basename(input_path))[0]
                    generated_pdf = os.path.join(out_dir, base_name + ".pdf")
                    if generated_pdf != output_path and os.path.exists(generated_pdf):
                        os.replace(generated_pdf, output_path)
                    return output_path

        # Fallback using python-docx & PyMuPDF
        doc = Document(input_path)
        pdf_doc = fitz.open()
        page = pdf_doc.new_page()
        y = 50
        for para in doc.paragraphs:
            if para.text.strip():
                if y > 750:
                    page = pdf_doc.new_page()
                    y = 50
                page.insert_text(fitz.Point(50, y), para.text[:100], fontsize=11, color=(0, 0, 0))
                y += 20
        pdf_doc.save(output_path)
        pdf_doc.close()
        return output_path

    @staticmethod
    def pptx_to_pdf(input_path, output_path):
        if PDFTools.has_libreoffice():
            for cmd in ["libreoffice", "soffice"]:
                if subprocess.run(["which", cmd], capture_output=True).returncode == 0:
                    out_dir = os.path.dirname(output_path)
                    subprocess.run([cmd, "--headless", "--convert-to", "pdf", input_path, "--outdir", out_dir], check=True)
                    base_name = os.path.splitext(os.path.basename(input_path))[0]
                    generated_pdf = os.path.join(out_dir, base_name + ".pdf")
                    if generated_pdf != output_path and os.path.exists(generated_pdf):
                        os.replace(generated_pdf, output_path)
                    return output_path

        # Fallback using python-pptx & PyMuPDF
        prs = Presentation(input_path)
        pdf_doc = fitz.open()
        for slide in prs.slides:
            page = pdf_doc.new_page()
            y = 50
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for p in shape.text_frame.paragraphs:
                        if p.text.strip():
                            if y > 750:
                                page = pdf_doc.new_page()
                                y = 50
                            page.insert_text(fitz.Point(50, y), p.text[:100], fontsize=12, color=(0, 0, 0))
                            y += 25
        pdf_doc.save(output_path)
        pdf_doc.close()
        return output_path

    @staticmethod
    def pdf_to_docx(input_path, output_path):
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
        return output_path

    @staticmethod
    def pdf_to_pptx(input_path, output_path):
        doc = fitz.open(input_path)
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(10), Inches(5.625)
        blank_layout = prs.slide_layouts[6]

        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img_path = "/tmp/pdf_slide_temp.png"
            pix.save(img_path)
            slide = prs.slides.add_slide(blank_layout)
            slide.shapes.add_picture(img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
            if os.path.exists(img_path):
                os.remove(img_path)

        doc.close()
        prs.save(output_path)
        return output_path
