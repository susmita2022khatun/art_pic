from bgm_rem import remove_background
from num_image import numerize_image

def process_image(image_path, text_dir, output_dir, text_choice):
    """
    Full pipeline: Background Removal → Binary Conversion → Numbering.

    Args:
        image_path (str): Path to the input image.
        text_dir (str): Directory containing text files with numbers.
        output_dir (str): Directory to save output images.
        text_choice (str): Name of the text file (without extension) for numbering.

    Returns:
        str: Path to the final processed image.
    """
    print("Starting processing...")

    no_bg_path = remove_background(image_path)
    if no_bg_path is None:
        return None

    final_image_path = numerize_image(no_bg_path, text_dir, output_dir, text_choice)

    return final_image_path