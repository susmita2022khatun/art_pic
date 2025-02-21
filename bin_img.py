from lib import *

def binary_image_conversion(image_path):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    _, binary_img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    output_path = f"static/outputs/bin_{os.path.basename(image_path)}"
    cv.imwrite(output_path, binary_img)
    print(f"Binary image saved to {output_path}")
    return output_path
