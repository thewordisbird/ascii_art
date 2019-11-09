import os
from PIL import Image

# 1. Read image and print image size
def load_image(jpg_file):
    if jpg_file:
        im = Image.open(jpg_file)
        if im:
            print('Sucessfully loaded image!')
            return im
        else:
            print('Unable to load image.')
    return None 

def image_info(image):
    print(f'Image size: {image.size[0]} x {image.size[1]}')

# 2. Load images pixel data into a 2-d array
def image_to_pixels(image):
    pixel_matrix = []
    pixel_matrix_width = image.size[0]
    pixel_matrix_height = image.size[1]
    print(pixel_matrix_height, pixel_matrix_width)
    
    pixels = image.load()
    for i in range(pixel_matrix_width):
        pixel_row = []
        for j in range(pixel_matrix_height):
            pixel_row.append(pixels[i, j])
        pixel_matrix.append(pixel_row)
    
    return pixel_matrix

def pixel_matrix(image):
    '''Returns a flattened array of pixel data.'''
    print(list(image.getdata()))

# 3. Create brightness matrix
def average_brightness(pixel):
    return (pixel[0] + pixel[1] + pixel[2] / 3)

def lightness(pixel):
    return (max(pixel[0] + pixel[1] + pixel[2]) + min(pixel[0] + pixel[1] + pixel[2])) / 2

def luminosity(pixel):
    return (0.21 * pixel[0]) + (0.72 * pixel[1]) + (0.07 * pixel[2])
          


if __name__ == "__main__":
    # Get relative path to data folder for image file
    app_path = os.path.abspath(__file__)
    app_dir = os.path.dirname(app_path)
    parent_dir = os.path.dirname(app_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    jpg_image = os.path.join(data_dir, 'potato_head.jpg')

    image = load_image(jpg_image)
    image_info(image)
    image_to_pixels(image)
    
    