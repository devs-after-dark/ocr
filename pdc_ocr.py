#!/usr/bin/env python3

#import packages
import os
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import numpy as np

#file directory with pdfs
#filedir = r'<enter test file path here>'

def process_file(filedir):
    #loop through each file in file list and convert pdf's to images
    for file in os.listdir(filedir):
        #if file is a pdf then convert it to an image 
        if file.endswith(".pdf"):
                
            #get file path
            filepath = os.path.join(filedir, file)

            #get base file name without extension (this is for naming converted image file)
            (filename, ext) = os.path.splitext(os.path.basename(file))

            #create output image folder name
            imagefolder = os.path.join(filedir, filename)

            #prefix file name with file type: image
            filename = "image_" + filename

            #check if folder exists and if not create it
            try:
                os.mkdir(imagefolder)
            except:
                print('cant create folder')

            #convert pdf pages to images and store in corresponding image folder
            pages = convert_from_path(filepath, dpi=350, output_folder=imagefolder, fmt='jpg', output_file=filename)

        else:
            #imagefolder = filedir
            continue

    #loop through each image file in the folder
    for imagefile in os.listdir(imagefolder):
        if imagefile.endswith(".jpg"):
            #get image file path
            imgfilepath = os.path.join(imagefolder, imagefile)
            print(imgfilepath)
            #open file
            img1 = np.array(Image.open(imgfilepath))
            #extract text
            text = pytesseract.image_to_string(img1, config='-c preserve_interword_spaces=1 --oem 1 --psm 6')
            #text = pytesseract.image_to_string(img1)
            #trim text
            #text = text.strip()
            #create ouput file
            output_file_path = Path(os.path.join(imagefolder,'output.txt'))
            #open output file
            with output_file_path.open(mode="a") as output_file:
                output_file.write(text)
        else:
            continue
    return output_file_path
