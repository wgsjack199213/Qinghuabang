# -*- coding: UTF-8 -*-

from PIL import Image
from PIL import ImageChops
import time
import requests
import os
import sys
import pandas as pd

url_prefix = None

def download_img(url, path):
    r = requests.get(url)
    with open(path + '/' + url.split('/')[-1], 'wb') as f:
        f.write(r.content)      

def download_imgs(path):
    print "Start downloading the images~"

    with open(path) as fin:
        line = fin.readline().strip()
        urls = line[5:-6].split('[/img][img]')

        global url_prefix
        url_prefix = '/'.join(urls[0].split('/')[:-1])

        download_path = str(int(time.time()))
        os.mkdir(download_path)
        for url in urls:
            download_img(url, download_path)

    print "Downloading completed~"
    return download_path

def match_image(img_path, download_path):
    print "Start matching the images~"

    matching = {}
    checked = set()
    
    images_1 = os.listdir(img_path)
    images_2 = os.listdir(download_path)

    # Neglect the hidden files such as .DS_Store
    images_1 = filter(lambda f: f[0] != '.', images_1) 
    images_2 = filter(lambda f: f[0] != '.', images_2) 
    
    if len(images_1) != len(images_2):
        raise Exception("The two folders contain differen number of files:\n" + 
                        img_path + ' and ' + download_path)

    for f1 in images_1:
        print '- Processing', f1
        for f2 in images_2:
            if f2 in checked:
                continue
            img1 = Image.open(img_path + '/' + f1)
            img2 = Image.open(download_path + '/' + f2)
            if img1.size != img2.size:
                continue

            try: 
                diff = ImageChops.difference(img1, img2)
                if diff.getbbox() is None:
                    matching[f1] = f2
                    checked.add(f2)
            except:
                continue

    print "Matching completed."
    return matching
    
def generate_md(matching, csv_path):
    print "Start generating the markdown output file."

    df = pd.read_csv(csv_path)

    output_str = ""
    for index in xrange(len(df)):
        ID = df.iloc[index]['编号']
        desc = df.iloc[index]['1.任务描述、报酬']
        image_url = df.iloc[index]['3.图片']
    
        #print ID
        #print desc
        output_str += str(ID) + ' ' + desc + '\n'
    
        if type(image_url) == str:
            image_file = image_url.split('"')[-2]
            #print image_file
            global url_prefix
            output_str += "\n<img src=\"" + url_prefix + '/' + matching[image_file] + "\" width=\"300\" align=center />\n"
        output_str += '\n-\n'

    with open('output.md', 'w') as fout:
        fout.write(output_str)

    print "md file generation completed."

        

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python match_imgs.py PATH_TO_THE_IMAGE_DIRECTORY PATH_TO_THE_CSV_FILE"
        print "Example: python match_imgs.py /Users/wgs/Desktop/QHB/q-3-rmUj /Users/wgs/Desktop/QHB/1986149_seg_1.csv"
    else:
        url_file = 'images.txt'
        download_path = download_imgs(url_file)
        #download_path = "1540136983" 

        matching = match_image(sys.argv[1], download_path)

        generate_md(matching, sys.argv[2])

        print "Comeletion!"

