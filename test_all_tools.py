import os
import shutil
from pdfworks_studio.tools import PDFTools

test_dir = "/home/deesspanda/Personal Data/1 Clg/Notes/DC/2 & 3"
output_test_dir = "/tmp/pdfworks_test_output"

if os.path.exists(output_test_dir):
    shutil.rmtree(output_test_dir)
os.makedirs(output_test_dir, exist_ok=True)

sample_pdf = os.path.join(test_dir, "Magnitude Comparator, Decoder, Encoder, Priority Encoder.pdf")
sample_pptx = os.path.join(test_dir, "Unit II Combinational Logic Circuits.pptx")

print("--- Testing PDFWorks Studio Tools ---")

# 1. Compress PDF
print("Testing Compress PDF...")
out_compress = os.path.join(output_test_dir, "compressed.pdf")
PDFTools.compress_pdf(sample_pdf, out_compress)
assert os.path.exists(out_compress)
print("✓ Compress PDF passed")

# 2. Rotate PDF
print("Testing Rotate PDF...")
out_rotate = os.path.join(output_test_dir, "rotated.pdf")
PDFTools.rotate_pdf(sample_pdf, out_rotate, 90)
assert os.path.exists(out_rotate)
print("✓ Rotate PDF passed")

# 3. Protect & Unlock PDF
print("Testing Protect & Unlock PDF...")
out_protect = os.path.join(output_test_dir, "protected.pdf")
out_unlock = os.path.join(output_test_dir, "unlocked.pdf")
PDFTools.protect_pdf(sample_pdf, out_protect, "testpwd")
PDFTools.unlock_pdf(out_protect, out_unlock, "testpwd")
assert os.path.exists(out_unlock)
print("✓ Protect & Unlock PDF passed")

# 4. Watermark PDF
print("Testing Watermark PDF...")
out_watermark = os.path.join(output_test_dir, "watermarked.pdf")
PDFTools.watermark_pdf(sample_pdf, out_watermark, "CONFIDENTIAL")
assert os.path.exists(out_watermark)
print("✓ Watermark PDF passed")

# 5. Extract Images
print("Testing Extract Images...")
out_img_dir = os.path.join(output_test_dir, "extracted_imgs")
images = PDFTools.extract_images(sample_pdf, out_img_dir)
print(f"✓ Extract Images passed (extracted {len(images)} images)")

# 6. Split PDF
print("Testing Split PDF...")
out_split_dir = os.path.join(output_test_dir, "split_pages")
split_files = PDFTools.split_pdf(sample_pdf, out_split_dir, mode="all")
print(f"✓ Split PDF passed (created {len(split_files)} pages)")

# 7. PowerPoint to PDF
print("Testing PowerPoint to PDF...")
out_pptx_pdf = os.path.join(output_test_dir, "presentation.pdf")
PDFTools.pptx_to_pdf(sample_pptx, out_pptx_pdf)
assert os.path.exists(out_pptx_pdf)
print("✓ PowerPoint to PDF passed")

print("\nAll tests completed successfully with zero errors!")
