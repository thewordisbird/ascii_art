
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
        
                       A            SSSSSSS        CCCCCCC   IIIIIIIII  IIIIIIIII
                      AAA         SSSS   SSSS    CCCC  CCCC     III        III
                     AAAAA        SSS     SSS   CCC     CCC     III        III 
                    AAA AAA        SSSSS        CCC             III        III 
                   AAA   AAA          SSSSS     CCC             III        III     
                  AAAAAAAAAAA           SSSS    CCC             III        III     
                 AAAAAAAAAAAAA    SSS     SSS   CCC     CCC     III        III 
                AAA         AAA   SSSS   SSSS    CCCC  CCCC     III        III 
               AAA           AAA    SSSSSSS        CCCCCC    IIIIIIIII  IIIIIIIII