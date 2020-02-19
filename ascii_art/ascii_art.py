import os
from subprocess import Popen, PIPE
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
    def __init__(self, image_path):
        #self.ascii_chars = ' `^",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
        self.ascii_chars = ' `":i|nhH0#'
        self.x_scale = 1
        self.y_scale = 2
        self.brightness_calc = 'average'
        self.inverse = False
        self.image = Image.open(image_path)

    def print_to_terminal(self):
        """
        Prints ascii_arr to terminal

        Parameters:
            ascii_arr (list obj): list of ascii characters.
            image_width (int):
            image_height (int):
        """
        for ascii_row in self.process_ascii_art('terminal'):
            print(ascii_row)

    def print_to_file(self, path):
        """
        Saves ascii_arr to .txt file

        Parameters:
            ascii_arr (list obj): list of ascii characters.
            image_width (int):
            image_height (int):
        """
        with open(path + '/ascii_art.txt', 'w') as f:            
            for ascii_row in self.process_ascii_art('file'):
                    f.write(ascii_row + "\n")
    

    def process_ascii_art(self, destination):
        """
        Glue funciton takes PIL image object and calculates brightness for each pixel depending on 
        the desired calculation. It also determines the brightness range to get better contrast. 
        Lastly, an ascii character is determined and added to a new array,

        Parameters:
            

        Returns:
            ascii_arr, image_widt, image_height (tuple): 

        Dependencies:
            brightness_calc: This is a funciton object that is passed in at run time.
            brightness_to_char:
        """
        # Scale image for output
        if destination == 'terminal':
            # Output to terminal
            terminal_scale = self.scale_for_terminal()
            (new_width, new_height) = (self.image.width//(self.x_scale * terminal_scale), self.image.height//(self.y_scale * terminal_scale))
            
        else:
            # Output to file (8.5 X 11 assumed)
            page_scale = self.scale_for_page()
            (new_width, new_height) = (self.image.width//(self.x_scale * page_scale), self.image.height//(self.y_scale * page_scale))

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
            #ascii_arr.append(ascii_char)
        #return ascii_arr, image.size[0], image.size[1]

    def scale_for_terminal(self):
        term_size = Popen('stty size', shell=True, stdout=PIPE)
        term_height, term_width = map(lambda n: int(n.decode('utf-8')) - 1, term_size.communicate()[0].split())
        
        # Scale for terminal character size (based on x_scale and y_scale attribute)
        img_width = self.image.width // self.x_scale
        img_height = self.image.height // self.y_scale
        
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

            return img_width // output_width


    def scale_for_page(self):
        page_width = 150
        page_height = 150

        # Scale for page character size (based on x_scale and y_scale attribute)
        img_width = self.image.width // self.x_scale
        img_height = self.image.height // self.y_scale
        
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

                
    # --- NEEDS TESTING ---
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


    # Print and/or display methods
    



if __name__ == "__main__":
    # Get relative path to data folder for image file
    app_path = os.path.abspath(__file__)
    app_dir = os.path.dirname(app_path)
    parent_dir = os.path.dirname(app_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    jpg_image = os.path.join(data_dir, 'm.jpg')

    a = AsciiArt(jpg_image)
    a.print_to_terminal()

