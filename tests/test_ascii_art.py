import os
import pytest
from PIL import Image

from ascii_art import Brightness, AsciiArt, test

# Need to setup test image fixture to save image and delete it after teseting. 

# Need to setup app as editable package so it can be imported for testing
    
@pytest.fixture(scope='function')
def test_image():
    test_pixel_matrix = [
                            [(254, 0, 0), (0, 254, 0), (0, 0, 254)],
                            [(254, 0, 0), (0, 254, 0), (0, 0, 254)],
                            [(254, 0, 0), (0, 254, 0), (0, 0, 254)]
                        ]
    im = Image.new('RGB', (3, 3))
    px = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            print(f'Before: {i,j} | {px[i,j]}')
            px[i,j] = test_pixel_matrix[i][j]
            print(f'After: {i,j} | {px[i,j]}')

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            print(f'Pixel at: {i,j} | {px[i,j]}')
            
    # save test image in test file while testing
    test_image_path = os.path.join(os.path.dirname(os.path.join(os.path.abspath(__file__))), 'test_img.png')
    print(test_image_path)
    im.save(test_image_path)
    yield test_image_path

    # Delete image file
    os.remove(test_image_path)



def test_constuct_AsciiArt_class(test_image):
    a = AsciiArt(test_image)
    assert a.image.width == 3
    assert a.image.height == 3

@pytest.mark.parametrize('test_width, test_height, scale',
                        [
                            (500, 200, 1)

                        ])
def test_scale_for_terminal(test_image, monkeypatch, test_width, test_height, scale):
    a = AsciiArt(test_image)
    
    # monkeypatch terminal size
    monkeypatch.setattr(os.popen('stty size', 'r'), 'read()', lambda: f'{test_width} {test_height}')
    

    assert a.scale_for_terminal() == scale




def test_test(monkeypatch):

    def mock_size():
        return '2 2\n'
    # monkeypatch terminal size
    monkeypatch.setattr(os.popen('stty size', 'r'), 'read', mock_size)

    assert test() == '2 2'











def test_resize_image(test_image):
    # GIVEN a path to an image (png or jpg)
    # WHEN passed to the load image function
    # THEN the image will be converted to a PIL Image
    a = AsciiArt(test_image, x_scale=1, y_scale=1)
    a.resize_image()
    a_width, a_height = a.image.size[0], a.image.size[1]
    img = Image.open(test_image)

    assert a_width == img.size[0]
    assert a_height == img.size[1]


def test_image_info(test_image, capsys):
    # GIVEN a PIL Image object
    # WHEN the image_info function is called on the PIL Image object.
    # THEN the width and height of the image will be printed
    img = Image.open(test_image)
    a = AsciiArt(test_image, x_scale=1, y_scale=1)
    a.image_info()
    captured = capsys.readouterr()
    assert captured.out == f'Image size: {img.size[0]} x {img.size[1]}\n'

@pytest.mark.parametrize('mode, pixel, result',
                        [
                            ('average', (123, 34, 211), 122),
                            ('ave', (123, 34, 211), 122),
                            ('', (123, 34, 211), 122),
                            ('lightness', (123, 34, 211), 122),
                            ('luminosity', (123, 34, 211), 65),

                        ])
def test_brightness_calc(mode, pixel, result):
    # GIVEN a brightness calculation
    # WHEN the brightness object is passed a pixel tuple
    # THEN the calc method of the brightness class will calculate
    # the brightness based on the set calculation mode attribute

    bc = Brightness(mode)
    assert bc.calc(pixel) == result


# MOVE ASCII CHARS OUTSIDE OF FUNCTION
@pytest.mark.parametrize('brightness, brightness_range, inverse, char', 
                        [
                            (0, 255, False, '0' ),
                            (0, 255, True, '5'),
                            (135, 255, False, '3'),
                            (135, 255, True, '2'),
                            (225, 255, False, '4'),
                            (225, 255, True, '1'),
                            (255, 255, False, '5'),
                            (255, 255, True, '0'),
                        ])
def test_brightness_to_char(brightness, brightness_range, inverse, char):
    ascii_chars = '012345'
    assert a.brightness_to_char(brightness, brightness_range, inverse, ascii_chars) == char
