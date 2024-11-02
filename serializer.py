#!/usr/bin/env python3

import sys
import os
import base64
import mimetypes
import argparse
from bs4 import BeautifulSoup
from PIL import Image
import io

def compress_image(image_path, compress_level):
    try:
        img = Image.open(image_path)
        img_format = img.format  # Preserve the original image format
        img_bytes = io.BytesIO()

        if img_format == 'JPEG' or img_format == 'JPG':
            # For JPEG, adjust the quality parameter
            quality = max(1, 100 - compress_level * 10)
            img.save(img_bytes, format='JPEG', quality=quality, optimize=True)
        elif img_format == 'PNG':
            # For PNG, adjust the compression level (0-9)
            # In Pillow, a higher compress_level means more compression
            compress_level_pillow = min(9, compress_level)
            img.save(img_bytes, format='PNG', compress_level=compress_level_pillow, optimize=True)
        else:
            # For other formats, we may not be able to compress
            img.save(img_bytes, format=img_format)

        img_bytes.seek(0)
        return img_bytes.read()
    except Exception as e:
        print(f"Error compressing image {image_path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Serialize HTML images into base64.')
    parser.add_argument('input_html', help='Input HTML file')
    parser.add_argument('-c', '--compress', type=int, choices=range(1, 11),
                        help='Compression level from 1 (10%) to 10 (100%)')
    args = parser.parse_args()

    html_file = args.input_html
    compress_level = args.compress if args.compress else 0  # Default to 0 if not specified
    html_dir = os.path.dirname(os.path.abspath(html_file))

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if not src:
            continue
        # Skip data URIs
        if src.startswith('data:'):
            continue
        # Skip absolute URLs
        if src.startswith('http://') or src.startswith('https://'):
            continue
        # Build the full path to the image file
        img_path = os.path.join(html_dir, src)
        if not os.path.exists(img_path):
            print(f"Image file {img_path} not found.")
            continue

        # Compress the image if compression level is specified
        if compress_level > 0:
            img_data = compress_image(img_path, compress_level)
            if img_data is None:
                continue  # Skip if compression failed
        else:
            with open(img_path, 'rb') as img_file:
                img_data = img_file.read()

        img_base64 = base64.b64encode(img_data).decode('utf-8')
        mime_type, _ = mimetypes.guess_type(img_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        data_uri = f'data:{mime_type};base64,{img_base64}'
        img_tag['src'] = data_uri

    # Output the modified HTML to a new file
    base_name, ext = os.path.splitext(html_file)
    output_file = f"{base_name}_serialized{ext}"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Serialized HTML written to {output_file}")

if __name__ == '__main__':
    main()
