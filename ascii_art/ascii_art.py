import os
import csv
from PIL import Image

# 1. Read image and print image size
def load_image(jpg_file, x_scale=1, y_scale=1):
    if jpg_file:
        im = Image.open(jpg_file)
        if im:
            (width, height) = (im.width//x_scale, im.height//y_scale)
            im = im.resize((width, height))
            return im
        else:
            print('Unable to load image!')
            return None 

def image_info(image):
    print(f'Image size: {image.size[0]} x {image.size[1]}')

# 2. Load images pixel data into a 2-d array
def build_pixel_matrix(image):
    # image.getdata() returns a 1-D array
    # When refactoring consider list composition to make code more pythonic
    pixel_matrix = []
    pixel_matrix_width = image.size[0]
    pixel_matrix_height = image.size[1]
    
    pixels = image.load()
    for i in range(pixel_matrix_width):
        pixel_row = []
        for j in range(pixel_matrix_height):
            pixel_row.append(pixels[i, j])
        pixel_matrix.append(pixel_row)
    
    return pixel_matrix


# 3. Create brightness matrix
def average_brightness(pixel):
    return (pixel[0] + pixel[1] + pixel[2]) / 3

def lightness(pixel):
    return (max(pixel[0], pixel[1], pixel[2]) + min(pixel[0], pixel[1], pixel[2])) / 2

def luminosity(pixel):
    return (0.21 * pixel[0]) + (0.72 * pixel[1]) + (0.07 * pixel[2])

def build_brightness_matrix(pixel_matrix, filter=average_brightness):
    brightness_matrix = []
    for row in pixel_matrix:
        brightness_matrix_row = []
        for pixel in row:
            brightness_matrix_row.append(round(filter(pixel), 0))
        brightness_matrix.append(brightness_matrix_row)
    
    return brightness_matrix
            
# 4. Convert brightness to ascii character
def brightness_to_char(brightness, inverse):
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    if inverse:
        ascii_chars = ''.join([ascii_chars[i] for i in range(len(ascii_chars) - 1, -1, -1)])

    return ascii_chars[int(brightness % len(ascii_chars))]
          
def build_char_matrix(brightness_matrix, inverse=False):
    char_matrix = []
    for row in brightness_matrix:
        char_matrix_row = []
        for brightness in row:
            char_matrix_row.append(brightness_to_char(brightness, inverse))
        char_matrix.append(char_matrix_row)
    
    return char_matrix

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


def full_build(image, brightness_type=average_brightness, inverse=False):
    row_string = ''
    for i, p in enumerate(image.getdata()):
        brightness = brightness_type(p)
        ascii_char = brightness_to_char(brightness, inverse)
        if i % image.size[0] - 1 == 0:
            print(row_string + ascii_char)
            row_string = ''
        else:
            row_string = row_string + ascii_char


class Pixel:
    def __init__(self, rgb_pixel):
        self.rgb_pixel = rgb_pixel
        self.ascii_char = None

    def average_brightness(self):
        return (rgb_pixel[0] + rgb_pixel[1] + rgb_pixel[2]) / 3

    def lightness(self):
        return (max(rgb_pixel[0], rgb_pixel[1], rgb_pixel[2]) + min(rgb_pixel[0], rgb_pixel[1], rgb_pixel[2])) / 2

    def luminosity(self):
        return (0.21 * rgb_pixel[0]) + (0.72 * rgb_pixel[1]) + (0.07 * rgb_pixel[2])

    def set_ascii_char(self, brightness_filter):
        




class AsciiArt:
    def __init__(self, image):
        self.image = image     
        self.x_scale = 1
        self.y_scale = 1
        self.brightness_type = average_brightness
        self.inverse = False
        self.ascii_image = self.load_ascii_image()

    def load_image(self, image_path):
        return Image.open(jpg_file)

    def load_ascii_image(self):
        pass

    def print_to_terminal(self):
        pass

    def save_as_txt_file(self):
        pass


    def scale_image(self, x_scale, y_scale))
        # modifies image... consider creating new object
        (width, height) = (self.image.width//x_scale, self.image.height//y_scale)
        self.image = self.image.resize((width, height))
    
    def get_pixel_brightness(self, rgb_pixel):
        return self.brightness_type(rgb_pixel)

    

    def get_ascii_char(self, pixel_brightness):
        ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        if self.inverse:
            ascii_art = [ascii_chars[i] for i in range(len(ascii_chars)-1, -1, -1)]

        return ascii_chars[int(pixel_brightness % len(ascii_chars))]
        

        





if __name__ == "__main__":
    # Get relative path to data folder for image file
    app_path = os.path.abspath(__file__)
    app_dir = os.path.dirname(app_path)
    parent_dir = os.path.dirname(app_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    jpg_image = os.path.join(data_dir, 'potato_head.jpg')
    jpg_image = os.path.join(data_dir, 'download.jpeg')

    image = load_image(jpg_image, 2,1)
    image_info(image)
    pixel_matrix = build_pixel_matrix(image)
    brightness_matrix = build_brightness_matrix(pixel_matrix, lightness)
    char_matrix = build_char_matrix(brightness_matrix, True)
    #save_ascii_art(char_matrix)
    #print_to_terminal(char_matrix)

    #full_build(image, average_brightness, True)
    
    # TODO:
    # Image seems to be rotates left by 90
    # Hard Code scaling factor
    # Build tests
    # Refactor by simplifying. Can go from pixel to char in one function.

    # Object Oriented package for flask app
    
    # Bonos sections on project