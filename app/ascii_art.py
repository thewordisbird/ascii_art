import os
from PIL import Image

# 1. Read image and print image size
def load_image(jpg_file):
    im = Image.open(jpg_file)
    if im:
        print('Sucessfully loaded image!')
        return im
    else:
        print('Unable to load image.')

def image_info(image):
    print(f'Image size: {image.size[0]} x {image.size[1]}')

if __name__ == "__main__":
    # Get relative path to data folder for image file
    app_path = os.path.abspath(__file__)
    app_dir = os.path.dirname(app_path)
    parent_dir = os.path.dirname(app_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    jpg_image = os.path.join(data_dir, 'potato_head.jpg')

    image = load_image(jpg_image)
    image_info(image)
    