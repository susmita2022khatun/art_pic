from lib import *

def remove_background(input_path, output_path):
    input_data = open(input_path, "rb").read()
    output_data = rembg.remove(input_data)

    nparr = np.frombuffer(output_data, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_UNCHANGED)

    if img.shape[2] == 4:
        b, g, r, a = cv.split(img)
        white_bg = np.ones_like(img, dtype=np.uint8) * 255
        alpha_factor = a.astype(np.float32) / 255.0
        for c in range(3):
            white_bg[:, :, c] = white_bg[:, :, c] * (1 - alpha_factor) + img[:, :, c] * alpha_factor
        img = white_bg[:, :, :3]

    cv.imwrite(output_path, img)
    print(f"Background Removed: {output_path}")