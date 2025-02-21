from lib import *
from bin_img import binary_image_conversion

def numerize_image(image_path, text_dir, output_dir, choice):
    """
    Overlays numbers from a text file onto a grid-based image.

    Args:
        image_path (str): Path of the input image.
        text_dir (str): Directory containing text files with numbers.
        output_dir (str): Directory to save output images.
        choice (str): Name of the text file (without extension) to use for numbering.

    Returns:
        str: Path to the final numbered image.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    binary_path = binary_image_conversion(image_path)
    if binary_path is None:
        return None

    text_file_path = os.path.join(text_dir, f"{choice}.txt")
    if not os.path.exists(text_file_path):
        print(f"Error: {text_file_path} not found.")
        return None

    with open(text_file_path, 'r') as f:
        numbers = f.read().replace(" ", "").strip()

    img = cv.imread(image_path)
    if img is None:
        print(f"Warning: Unable to read {image_path}. Skipping.")
        return None

    original_height, original_width = img.shape[:2]

    # Resize while maintaining aspect ratio
    if original_height > original_width:
        new_width = int(original_width * (MAX_DIM / original_height))
        new_height = MAX_DIM
    else:
        new_height = int(original_height * (MAX_DIM / original_width))
        new_width = MAX_DIM

    grid_image = np.full((new_height, new_width), 255, dtype=np.uint8)
    binary_img = cv.imread(binary_path, cv.IMREAD_GRAYSCALE)
    binary_img = cv.resize(binary_img, (new_width, new_height))

    cell_index = 0
    for i in range(0, new_height, GRID_SIZE):
        for j in range(0, new_width, GRID_SIZE):
            if binary_img[i:i + GRID_SIZE, j:j + GRID_SIZE].mean() < 128:
                if cell_index < len(numbers):
                    current_number = numbers[cell_index]
                    center_x = j + GRID_SIZE // 2
                    center_y = i + GRID_SIZE // 2
                    cv.putText(grid_image, current_number, (center_x, center_y),
                               cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1, lineType=cv.LINE_AA)
                    cell_index += 1

    output_filename = f"grid_image_{os.path.basename(image_path)}"
    output_path = os.path.join(output_dir, output_filename)
    cv.imwrite(output_path, grid_image)

    print(f"Grid image saved to {output_path}")
    print(f"Total numbers placed: {cell_index}")
    
    return output_path
