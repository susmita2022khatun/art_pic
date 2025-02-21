from utils import *

input_image = "test_img/1721499053016.jpeg"  # Replace with actual image
text_directory = "numbers"  # Directory containing text files
output_directory = "final_output"
text_filename = "pi"  # Replace with actual text file (without .txt)

final_result = process_image(input_image, text_directory, output_directory, text_filename)

if final_result:
    print(f"Processing Complete: {final_result}")
