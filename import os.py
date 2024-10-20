import os
import base64

def encode_image_to_base64(image_path):
    """Encodes an image file to a Base64 string."""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def generate_minute_constants(images_dir):
    """Generates JavaScript constants for minutes 1 to 15."""
    constants = []
    for minute in range(1, 16):
        image_file = f'minute{minute}.png'
        image_path = os.path.join(images_dir, image_file)
        if os.path.isfile(image_path):
            base64_str = encode_image_to_base64(image_path)
            ext = os.path.splitext(image_file)[1].lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp'
            }
            mime = mime_types.get(ext, 'application/octet-stream')
            data_url = f'data:{mime};base64,{base64_str}'
            constants.append(f"const minute{minute} = '{data_url}';")
        else:
            constants.append(f"const minute{minute} = '';")
    return constants

def insert_constants_into_html(html_file, constants):
    """Inserts the minute constants into the HTML file."""
    with open(html_file, 'r') as file:
        content = file.read()

    # Find the script block to insert constants before the main script
    script_start = content.find('<script>')
    script_end = content.find('</script>', script_start)
    if script_start == -1 or script_end == -1:
        print("Error: <script> tag not found in the HTML file.")
        return

    # Insert constants after the opening <script> tag
    insertion_point = script_start + len('<script>')
    constants_block = '\n'.join(constants) + '\n'
    new_content = content[:insertion_point] + '\n' + constants_block + content[insertion_point:]

    with open(html_file, 'w') as file:
        file.write(new_content)

    print(f"Successfully inserted {len(constants)} minute constants into '{html_file}'.")

def main():
    # Directory containing images (current directory)
    images_dir = '.'

    # Define the HTML file to update
    html_file = 'index.html'

    # Check if the HTML file exists
    if not os.path.isfile(html_file):
        print(f"Error: '{html_file}' does not exist in the current directory.")
        return

    # Generate the minute constants
    minute_constants = generate_minute_constants(images_dir)

    # Insert the constants into the HTML file
    insert_constants_into_html(html_file, minute_constants)

if __name__ == "__main__":
    main()
