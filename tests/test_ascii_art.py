import pytest
import os

from PIL import Image
#from app.ascii_art import load_image

# Need to setup test image fixture to save image and delete it after teseting. 

# Need to setup app as editable package so it can be imported for testing
@pytest.fixture
def test_image():
    test_pixel_matrix = [
        [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)],
        [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)],
        [(0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0)],
        [(0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0)],
        [(0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255)],
        [(0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255)]
    ]

    im = Image.new('RGB', (6, 4))
    px = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            print(i,j)
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

def test(test_image):
    tip = test_image
    assert tip == None