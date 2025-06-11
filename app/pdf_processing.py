import fitz
import os
os.environ['PYZBAR_LIBRARY_PATH'] = '/opt/homebrew/opt/zbar/lib/libzbar.dylib'

from pdf2image import convert_from_path
from pyzbar.pyzbar import decode

pdf_path = '../ticket.pdf'

document = fitz.open(pdf_path)

print("---------- TEXT CONTENT --------------\n")

for i, page in enumerate(document):
    text = page.get_text()
    print(f"\nPage{i+1}:\n{text}")

# --- Extract QR codes and save/display images ---
print("\n----- QR CODE DATA AND IMAGES -----")
pages = convert_from_path(pdf_path, dpi=300)

for i, page_image in enumerate(pages):
    decoded_objects = decode(page_image)
    if decoded_objects:
        for j, obj in enumerate(decoded_objects):
            if obj.type == 'QRCODE':
                # Print QR code data
                qr_data = obj.data.decode('utf-8')
                print(f"Page {i+1} QR Code {j+1}: {qr_data}")

                # Crop the QR code image from the page
                rect = obj.rect  # rect: left, top, width, height
                left, top, width, height = rect.left, rect.top, rect.width, rect.height
                qr_img = page_image.crop((left, top, left + width, top + height))

                # Save QR code image
                img_filename = f'outputs/qr_code_page{i+1}_{j+1}.png'
                qr_img.save(img_filename)
                print(f"Saved QR code image as {img_filename}")

                # Display QR code image (opens default image viewer)
                qr_img.show()
    else:
        print(f"Page {i+1}: No QR code found.")