import os
import csv

from PIL import Image




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
        

class AsciiArt:
    def __init__(self, image_path, **kwargs):
        #self.ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        self.ascii_chars = ' `":|hH0#'
        self.allowed_keys = {'x_scale', 'y_scale', 'brightness_calc', 'inverse'}
        #self.defaults = {'x_scale': 1, 'y_scale': 3, 'brightness_calc': 'average', 'inverse': False}
        self.x_scale = 1
        self.y_scale = 3
        self.brightness_calc = 'average'
        self.inverse = False
        
        for key, value in kwargs.items():
            if key in self.allowed_keys:
                setattr(self, key, value)
        
        self.image = Image.open(image_path)

        self.resize_image()

    def resize_image(self):
        """
        Resize PIL Image object.

        Parameters:
            img_path (str): Path to jpeg file.
            x_scale (int): Scale factor for image width. Defaults to 1.
            y_scale (int): Scale factor for image height. Defaults to 3.
        """
        (width, height) = (self.image.width // self.x_scale, self.image.height // self.y_scale)
        print(width, height)
        self.image = self.image.resize((width, height))
                


    def image_info(self):
        """
        Prints the PIL image object information.

        Parameters:
            image (Image obj): PIL image object of imported file.
        """
        if self.image:
            print(f'Image size: {self.image.size[0]} x {self.image.size[1]}')


    def brightness_to_char(self, brightness, brightness_range):
        """
        Determines ascii character to display based on brightness.

        Modify the ascii_chars string to change the resolution. 

        Parameters:
            brightness (float): Calculated brighness values between 0 and 255.
            brigtness_range (float): Max brightness - min brightness.
            inverse (bool): Trigger for weather or not the image is to be inverse.
            ascii_chars (str): String of ascii characters to use in ascii_art. 
                NOTE: For now this is in a global variable. This will eventually be 
                user customizable which is why the function is built this way

        Returns:
            ascii_char (str): Character from availible ascii_chars list.
        """
        
        if self.inverse:
            ascii_chars = self.ascii_chars[::-1] 
        else:
            ascii_chars = self.ascii_chars
        
        return ascii_chars[round(brightness * ((len(ascii_chars)-1)/brightness_range))]

    
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
        with open('data/ascii_art.txt', 'w') as f:
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
    
    #jpg_image = os.path.join(data_dir, 'zebra.jpg')
    #jpg_image = os.path.join(data_dir, 'face.jpeg')
    #jpg_image = os.path.join(data_dir, 'vans.png')
    jpg_image = os.path.join(data_dir, 'm.jpg')

    # For m
    image = load_image(jpg_image,14, 28)

    # For Zebra
    #image = load_image(jpg_image,3, 9)
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