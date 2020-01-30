import os
import csv
from PIL import Image


def load_image(img_path, x_scale=1, y_scale=3):
    """
    Create PIL Image object for jpeg/jpg image.

    Parameters:
        img_path (str): Path to jpeg file.
        x_scale (int): Scale factor for image width. Defaults to 1.
        y_scale (int): Scale factor for image height. Defaults to 3.
    """
    if img_path:
        img = Image.open(img_path)
        if img:
            (width, height) = (img.width // x_scale, img.height // y_scale)
            img = img.resize((width, height))
            return img
        else:
            print('Unable to load image!')
            return None 


def image_info(image):
    """
    Prints the PIL image object information.

    Parameters:
        image (Image obj): PIL image object of imported file.
    """
    if image:
        print(f'Image size: {image.size[0]} x {image.size[1]}')


# Convert brightness to ascii character
def brightness_to_char(brightness, brightness_range, inverse):
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    #ascii_chars = " `\":I!~_?[{)|/frnvzYJL0Zwpbho#W8B$"
    if inverse:
        ascii_chars = " " + ''.join([ascii_chars[i] for i in range(len(ascii_chars) - 1, -1, -1)])
    else:
        ascii_chars = ascii_chars + " "
    #print(int(brightness * ((len(ascii_chars)-1)/brightness_range)))
    return ascii_chars[int(brightness * ((len(ascii_chars)-1)/brightness_range))]


# Brightness Calculations
def average_brightness(pixel):
    return (pixel[0] + pixel[1] + pixel[2]) / 3

def lightness(pixel):
    return (max(pixel[0], pixel[1], pixel[2]) + min(pixel[0], pixel[1], pixel[2])) / 2

def luminosity(pixel):
    return (0.21 * pixel[0]) + (0.72 * pixel[1]) + (0.07 * pixel[2])

def full_build(image, brightness_calc, inverse=False):
    row_string = ''
    min_brightness = min(brightness_calc(pixel) for pixel in image.getdata())
    max_brightness = max(brightness_calc(pixel) for pixel in image.getdata())
    brightness_range = max_brightness - min_brightness

    for i, p in enumerate(image.getdata()):
        adjusted_brightness = brightness_calc(p) - min_brightness
        ascii_char = brightness_to_char(adjusted_brightness, brightness_range, inverse)
        if i % image.size[0] - 1 == 0:
            print(row_string + ascii_char)
            row_string = ''
        else:
            row_string = row_string + ascii_char



            
# Print and/or display methods
def save_ascii_art(char_matrix):
    with open('ascii_art.txt', 'w') as f:
        for row in char_matrix:
            f.write(''.join(row) + "\n")

def print_to_terminal(char_matrix):
    for row in char_matrix:
        row_string = ''
        for pixel in row:
            row_string = row_string + pixel
        print(row_string)

if __name__ == "__main__":
    # Get relative path to data folder for image file
    app_path = os.path.abspath(__file__)
    app_dir = os.path.dirname(app_path)
    parent_dir = os.path.dirname(app_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    #jpg_image = os.path.join(data_dir, 'zebra.jpg')
    #jpg_image = os.path.join(data_dir, 'face.jpeg')
    jpg_image = os.path.join(data_dir, 'vans.png')

    image = load_image(jpg_image, 6, 14)
    #image = load_image(jpg_image)

    #full_build(image, average_brightness, False)
    full_build(image, average_brightness, False)
    
    # TODO:
   
    # Write tests    

    # Object Oriented package for flask app
    
    # Bonos sections on project