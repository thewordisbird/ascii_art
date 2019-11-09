import pytest
import os

from PIL import Image
from ascii_art import ascii_art as a

# Need to setup test image fixture to save image and delete it after teseting. 

# Need to setup app as editable package so it can be imported for testing
    
@pytest.fixture(scope='function')
def test_image():
    test_pixel_matrix = [
        [(254, 0, 0), (254, 0, 0), (254, 0, 0), (254, 0, 0)],
        [(254, 0, 0), (254, 0, 0), (254, 0, 0), (254, 0, 0)],
        [(254, 0, 0), (254, 0, 0), (254, 0, 0), (254, 0, 0)],
        [(0, 254, 0), (0, 254, 0), (0, 254, 0), (0, 254, 0)],
        [(254, 0, 0), (254, 0, 0), (254, 0, 0), (254, 0, 0)],
        [(254, 0, 0), (254, 0, 0), (254, 0, 0), (254, 0, 0)]
    ]
    im = Image.new('RGB', (6, 4))
    px = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            print(test_pixel_matrix[i][j])
            px[i,j] = test_pixel_matrix[i][j]
    # save test image in test file while testing
    test_image_path = os.path.join(os.path.dirname(os.path.join(os.path.abspath(__file__))), 'test_img.jpg')
    print(test_image_path)
    im.save(test_image_path)
    yield test_image_path

    # Delete image file
    #os.remove(test_image_path)

#def test_load_image(test_image):
#    test_image_path = test_image
#    assert test_image_path != None

def test_fixture_construction(test_image):
    tip = "C:\\Users\\justi\\Desktop\\devel\\ascii_art\\tests\\test_img.jpg"
    assert tip == test_image

def test_load_image(test_image):
    assert a.load_image(test_image) != None

def test_image_info(test_image, capsys):
    im = Image.open(test_image)
    a.image_info(im)
    captured = capsys.readouterr()
    assert captured.out == f'Image size: {im.size[0]} x {im.size[1]}\n'

def test_image_to_pixels(test_image):
    im = Image.open(test_image)
    print(a.image_to_pixels(im))
    assert a.image_to_pixels(im) == [
        [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)],
        [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)],
        [(0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0)],
        [(0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0)],
        [(0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255)],
        [(0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255)]
    ]
