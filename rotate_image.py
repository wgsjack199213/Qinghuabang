import sys
import os
from PIL import Image

def process_directory(path):
    images = os.listdir(path)
    print 'Starting processing', len(images), 'images'

    print 'The results will be in ' + path + '_rotated'
    if not os.path.exists(path + '_rotated'):
        os.mkdir(path + '_rotated')

    
    for image in images:
        try:
            im = Image.open(path + '/' + image)
        except:
            print path + '/' + image + ' may not be an image?'
            continue

        width, height = im.size
        #print width, height
        if width < height * 0.9:
            im_rotate = im.rotate(90, expand=True)
            #im_rotate = im_rotate.resize((height, width))
            #im_rotate.show()

            im_rotate.save(path + '_rotated/' + image)
        else:
            im.save(path + '_rotated/' + image)

        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python rotate_image.py PATH_TO_THE_IMAGE_DIRECTORY"
        print "Example: python rotate_image.py /Users/wgs/Desktop/QHB/q-3-rmUj"
    else:
        process_directory(sys.argv[1])

    print "Completion~"
