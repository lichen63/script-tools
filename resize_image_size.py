import os
from PIL import Image

def resize_images_in_folder(input_folder, target_width):
    """
    Resize all images in the specified input folder to the target width,
    maintaining the aspect ratio. Save the resized images to a 'temp' folder in the current directory,
    with filenames modified to remove spaces and special characters.

    :param input_folder: Path to the input folder containing images.
    :param target_width: Desired width for resizing.
    """
    # Create the 'temp' folder in the current directory if it doesn't exist
    output_folder = os.path.join(os.getcwd(), "temp")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Check if the file is an image
        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                # Replace spaces and parentheses in the filename
                new_filename = filename.replace(" ", "_").replace("(", "").replace(")", "")
                
                # Form the new output path
                output_path = os.path.join(output_folder, new_filename)

                # Open the image
                with Image.open(input_path) as img:
                    # Get original dimensions
                    original_width, original_height = img.size
                    
                    # Calculate new height based on the aspect ratio
                    aspect_ratio = original_height / original_width
                    target_height = int(target_width * aspect_ratio)
                    
                    # Resize the image
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Save the resized image with the new filename
                    img.save(output_path)
                    print(f"Processed: {filename} -> {new_filename} (Original: {original_width}x{original_height}, Resized: {target_width}x{target_height})")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# User inputs
input_folder = input("Enter the path to the input folder: ")
try:
    target_width = int(input("Enter the target width (pixels): "))
    resize_images_in_folder(input_folder, target_width)
except ValueError:
    print("Invalid input! Please enter a numeric value for the target width.")