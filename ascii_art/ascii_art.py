import os
import math
from subprocess import Popen, PIPE
from PIL import Image


class Brightness:
    """Class to handle brightness calculations.

    Attributes:
        calc_mode: A dictionary mapping calc strings to their class method.
        calc: A string indicating which brightness calculation method to use.
    """

    def __init__(self, calc):
        """Inits the Brightness class.

        Args:
            calc: A string indicating which brightness calculation method to use. Defaults
            to 'average' if no string is provided or no item exists in the calc_mode dictionary.
        """

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
        return (pixel[0] + pixel[1] + pixel[2]) // 3

    
    def lightness(self, pixel):
        return (max(pixel[0], pixel[1], pixel[2]) + min(pixel[0], pixel[1], pixel[2])) // 2


    def luminosity(self, pixel):
        return int((0.21 * pixel[0]) + (0.72 * pixel[1]) + (0.07 * pixel[2]))
        

class AsciiArt:
    """Class to convert .jpg or .png image to ascii art.

    Attributes:
        ascii_chars: A string of ascii characters to be used in generating the image.
        x_calibrate: An int value to calibrate the output to the non-square character spacing of the terminal.
        y_calibrate: An int value to calibrate the output to the non-square characrer spacing of the terminal.
        brightness_calc: A string to designate the brightness calculation type.
        inverse: A boolean value to designate weather or not to inverse the ascii character string for image generation.
        image: A PIL Image object containing the imported image.

    Public Methods:
        print_to_terminal(): Prints the ascii art image to the terminal.
        print_to_file(): Prints the ascii art image to .txt file.
    """

    def __init__(self, image_path):
        """Inits the AsciiArt class.

        Loads a .jpg, .jpeg or .png image to a PIL Image to be processed as ascii art.
        Scaling defaults are set and image is set to false. These can be modified by 
        accessing the object attribute directly. i.e.

            a = AsciiArt('path/to/image')

            # To modify inverse:
            a.inverse = True

        Args:
            image_path: A string containing the path of the image to be processed.
        """

        #self.ascii_chars = ' `^",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
        self.ascii_chars = ' `":i|nhH0#'
        self.x_calibrate = 1
        self.y_calibrate = 2
        self.brightness_calc = 'average'
        self.inverse = False
        self.image = Image.open(image_path)


    def print_to_terminal(self):
        """Prints ascii_arr to terminal."""

        for ascii_row in self.process_ascii_art('terminal'):
            print(ascii_row)


    def print_to_file(self, path):
        """Saves ascii_arr to .txt file."""

        with open(path + '/ascii_art.txt', 'w') as f:            
            for ascii_row in self.process_ascii_art('file'):
                    f.write(ascii_row + "\n")
    

    def process_ascii_art(self, destination):
        # Glue function to take PIL Image object, calculate brightness for each pixel and map to an ascii character.
        # The function yields it's output at every completed row which is consumed by print_to_terminal() or 
        # print_to_file().
        
        # Scale image for output
        if destination == 'terminal':
            # Output to terminal
            terminal_scale = self.scale_for_terminal()
            (new_width, new_height) = (self.image.width//(self.x_calibrate * terminal_scale), self.image.height//(self.y_calibrate * terminal_scale))
            
        else:
            # Output to file (8.5 X 11 assumed)
            page_scale = self.scale_for_page()
            (new_width, new_height) = (self.image.width//(self.x_calibrate * page_scale), self.image.height//(self.y_calibrate * page_scale))

        # Create resized Image instance to process. 
        scaled_image = self.image.resize((int(new_width), int(new_height)))

        # Initiate brightness calc object
        bc = Brightness(self.brightness_calc)
        min_brightness = min(bc.calc(pixel) for pixel in scaled_image.getdata())
        max_brightness = max(bc.calc(pixel) for pixel in scaled_image.getdata())
        brightness_range = max_brightness - min_brightness
        
        # Build ascii_art pixel to char array
        ascii_row = []
        for i, p in enumerate(scaled_image.getdata()):
            if i % scaled_image.width - 1 == 0:
                yield ''.join(ascii_row)
                ascii_row = []
            else:
                adjusted_brightness = bc.calc(p) - min_brightness
                ascii_char = self.brightness_to_char(adjusted_brightness, brightness_range)
                ascii_row.append(ascii_char)
            

    def scale_for_terminal(self):
        term_size = Popen('stty size', shell=True, stdout=PIPE).communicate()
        term_height, term_width = map(lambda n: int(n) - 1, term_size[0].decode('utf-8').split())
        
        # Scale for terminal character size (based on x_calibrate and y_calibrate attribute)
        img_width = self.image.width // self.x_calibrate
        img_height = self.image.height // self.y_calibrate
        
        if img_width <= term_width and img_height <= term_height:
            return 1
        else:
            img_scale = img_width / img_height
            output_width = output_height = 0
            
            # Scale for availible terminal size. Needs to check based on width and height since both can vary
            if term_width / img_scale <= term_height:
                output_width = term_width
                output_height = term_width / img_scale

            if img_scale * term_height <= term_width and term_height > output_height:
                output_width = img_scale * term_height
                output_height = term_height

            return math.ceil(img_width / output_width)


    def scale_for_page(self):
        # Need to determine optimal 8.5 X 11 character dimensions.
        page_width = 150
        page_height = 150

        # Scale for page character size (based on x_calibrate and y_calibrate attribute)
        img_width = self.image.width // self.x_calibrate
        img_height = self.image.height // self.y_calibrate
        
        if img_width <= page_width and img_height <= page_height:
            return 1        
        else:
            img_scale = img_width / img_height
            output_width = output_height = 0
            
            # Scale for availible terminal size. Needs to check based on width and height since both can vary
            if page_width / img_scale <= page_height:
                output_width = page_width
                output_height = page_width / img_scale

            if img_scale * page_height <= page_width and page_height > output_height:
                output_width = img_scale * page_height
                output_height = page_height

            return img_width // output_width

            
    def image_info(self):
        """Prints the PIL image object information."""

        if self.image:
            print(f'Image size: {self.image.size[0]} x {self.image.size[1]}')


    def brightness_to_char(self, brightness, brightness_range):        
        if self.inverse:
            ascii_chars = self.ascii_chars[::-1] 
        else:
            ascii_chars = self.ascii_chars
        
        return ascii_chars[round(brightness * ((len(ascii_chars)-1)/brightness_range))]


if __name__ == "__main__":
    # Get relative path to data folder for image file
    app_path = os.path.abspath(__file__)
    app_dir = os.path.dirname(app_path)
    parent_dir = os.path.dirname(app_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    jpg_image = os.path.join(data_dir, 'm.jpg')

    a = AsciiArt(jpg_image)
    a.print_to_terminal()

