import os
import csv
from PIL import Image

class Test:
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)

class Brightness:
    """
    Class to handle brightness calculations.

    Parameters:
        calc (str): String name for calculation choice.
    """
    
    def __init__(self, calc):
        self.calc_mode = {
            "average": self.average_brightness,
            "lightness": self.lightness,
            "luminosity": self.luminosity
        }
        if calc in self.calc_mode:
            self.calc = self.calc_mode[calc]
        else:
            self.calc = self.calc_mode["average"]


    def average_brightness(self, pixel):
        """
        Calculates pixel brightness as the average of the RGB pixels.

        Parameters:
            pixel (tuple): (r, g, b) pixel information.

        Returns:
            average_brightness (float)
        """
        return (pixel[0] + pixel[1] + pixel[2]) // 3

    
    def lightness(self, pixel):
        """
        Calculates pixel brightness as the lightness of the RGB pixels.

        Parameters:
            pixel (tuple): (r, g, b) pixel information.

        Returns:
            lightness (float)
        """
        return (max(pixel[0], pixel[1], pixel[2]) + min(pixel[0], pixel[1], pixel[2])) // 2


    def luminosity(self, pixel):
        """
        Calculates pixel brightness as the luminosity of the RGB pixels.

        Parameters:
            pixel (tuple): (r, g, b) pixel information.

        Returns:
            luminosity (float)
        """
        return int((0.21 * pixel[0]) + (0.72 * pixel[1]) + (0.07 * pixel[2]))
        


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


def brightness_to_char(brightness, brightness_range, inverse):
    """
    Determines ascii character to display based on brightness.

    Modify the ascii_chars string to change the resolution. 

    Parameters:
        brightness (float): Calculated brighness values between 0 and 255.
        brigtness_range (float): Max brightness - min brightness.
        inverse (bool): Trigger for weather or not the image is to be inverse.

    Returns:
        ascii_char (str): Character from availible ascii_chars list.
    """
    # Found that fewer characters seem to display the image better.
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    #ascii_chars = " \":|H0#"
    if inverse:
        ascii_chars = " " + ''.join([ascii_chars[i] for i in range(len(ascii_chars) - 1, -1, -1)])
    else:
        ascii_chars = ascii_chars + " "
    
    return ascii_chars[int(brightness * ((len(ascii_chars)-1)/brightness_range))]




   
def build_ascii_arr(image, brightness_calc, inverse=False):
    """
    Glue funciton takes PIL image object and calculates brightness for each pixel depending on 
    the desired calculation. It also determines the brightness range to get better contrast. 
    Lastly, an ascii character is determined and added to a new array,

    Parameters:
        image (PIL Image Obj)
        brightness_calc (function obj): The desired brightness calculation method
        inverse (bool): Default set to false. 

    Returns:
        ascii_arr, image_widt, image_height (tuple): 

    Dependencies:
        brightness_calc: This is a funciton object that is passed in at run time.
        brightness_to_char:
    """
    # initiate brightness calc object
    bc = Brightness(brightness_calc)
    min_brightness = min(bc.calc(pixel) for pixel in image.getdata())
    max_brightness = max(bc.calc(pixel) for pixel in image.getdata())
    brightness_range = max_brightness - min_brightness
    ascii_arr = []
    for p in image.getdata():
        adjusted_brightness = bc.calc(p) - min_brightness
        ascii_char = brightness_to_char(adjusted_brightness, brightness_range, inverse)
        ascii_arr.append(ascii_char)
    return ascii_arr, image.size[0], image.size[1]


# Print and/or display methods
def save_ascii_art(ascii_arr, image_width, image_height):
    """
    Saves ascii_arr to .txt file

    Parameters:
        ascii_arr (list obj): list of ascii characters.
        image_width (int):
        image_height (int):
    """
    with open('ascii_art.txt', 'w') as f:
        ascii_row = []
        for i,p in enumerate(ascii_arr):
            if i % image_width - 1 == 0:
                ascii_row.append(p)
                f.write(''.join(ascii_row) + "\n")
                ascii_row = []
            else:
                ascii_row.append(p)


def print_to_terminal(ascii_arr, image_width, image_height):
    """
    Prints ascii_arr to terminal

    Parameters:
        ascii_arr (list obj): list of ascii characters.
        image_width (int):
        image_height (int):
    """
    ascii_row = ''
    for i, p in enumerate(ascii_arr):
        if i % image.size[0] - 1 == 0:
            print(ascii_row + p)
            ascii_row = ''
        else:
            ascii_row = ascii_row + p

if __name__ == "__main__":
    # Get relative path to data folder for image file
    app_path = os.path.abspath(__file__)
    app_dir = os.path.dirname(app_path)
    parent_dir = os.path.dirname(app_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    jpg_image = os.path.join(data_dir, 'zebra.jpg')
    #jpg_image = os.path.join(data_dir, 'face.jpeg')
    #jpg_image = os.path.join(data_dir, 'vans.png')
    #jpg_image = os.path.join(data_dir, 'm.jpg')

    #image = load_image(jpg_image,18, 28)
    image = load_image(jpg_image,3, 9)
    #image = load_image(jpg_image)

    #full_build(image, average_brightness, False)
    #ascii_arr, width, height = build_ascii_arr(image, "average", False)
    #ascii_arr, width, height = build_ascii_arr(image, "lightness", False)
    ascii_arr, width, height = build_ascii_arr(image, "luminosity", False)
   
    save_ascii_art(ascii_arr, width, height)
    print_to_terminal(ascii_arr, width, height)
    # TODO:
   
    # Write tests    

    # Object Oriented package for flask app
    
    # Bonos sections on project