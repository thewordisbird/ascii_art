import os
from PIL import Image

def build_image():
    test_pixel_matrix = [
                            [(254, 0, 0), (0, 254, 0), (0, 0, 254)],
                            [(254, 0, 0), (0, 254, 0), (0, 0, 254)],
                            [(254, 0, 0), (0, 254, 0), (0, 0, 254)]
                        ]

    im = Image.new('RGB', (3, 3))
    px = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            px_before = px[i,j]
            px[i,j] = test_pixel_matrix[i][j]
            print(f'Pixel at: {i,j} | Before: {px_before} | After: {px[i,j]}')

            
    # save test image in test file while testing
    test_image_path = os.path.join(os.path.dirname(os.path.join(os.path.abspath(__file__))), 'test_img.jpg')
    
    im.save(test_image_path)
    return test_image_path

def analyze_image(image_file):
    im = Image.open(image_file)
    width, height = im.size
    
    px = im.load()
    for i in range(width):
        for j in range(height):
            print(f'Pixel at: {i,j} | {px[i,j]}')
       
    
    #return pixel_matrix

    # Delete image file
    #os.remove(test_image_path)

if __name__ == "__main__":
    analyze_image(build_image())