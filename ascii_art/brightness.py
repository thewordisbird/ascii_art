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
        