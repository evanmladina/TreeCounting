# In[]


import glob
import random
import pandas as pd
import shutil
import os
import MakeNeonYoloAppropriate

from shutil import copyfile
from PIL import Image, ImageDraw
from pathlib import Path



# In[]


Image.MAX_IMAGE_PIXELS = None
_UTM_UNITS = 1000

# In[]

def crop_satellite_refactored(imPath, dim_x1, dim_y1):
    """
    dim_x1 and dim_y1 define the dimensions of each cropped image
    """
    im = Image.open(imPath)
    dim_x0, dim_y0 = im.size
    num_x = int(dim_x0/dim_x1)
    num_y = int(dim_y0/dim_y1)
    
    for i in range(0,num_x):
        for j in range(0, num_y):
            x_begin = i*dim_x1
            x_end = x_begin + dim_x1
            y_begin = j*dim_y1
            y_end = y_begin + dim_y1
            cropped = im.crop((x_begin, y_begin, x_end, y_end))
            cropped.save(f"tree_crop/images/{Path(imPath).stem}_{i}_{j}.jpg")


def write_labels_refactored(csvFilePath, impath, geosite, dim_x0, dim_y0, dim_x1, dim_y1):
    dataframe = pd.read_csv(csvFilePath)
    filtered_dataframe = dataframe.loc[dataframe['geo_index'] == geosite]
    xoffset, yoffset = map(int, geosite.split("_"))

    for _, (left,right,top,bottom) in filtered_dataframe[["left", "right", "top", "bottom"]].iterrows():
        #Get UTM coordinates
        #UTM y coordinates are given assuming origin is bottom left
        #We must flip them as Image assumes origin is top left
        startx = left - xoffset
        stopx = right - xoffset
        starty = _UTM_UNITS - (bottom - yoffset)  #TODO:  why are we subtracting from UTM units, which is always 1000
        stopy = _UTM_UNITS - (top - yoffset) # I think we should be subtractin from the size of the image, which in this case is dim_y1
                                             # If so, also change yolov5Annotation

        #Convert to pixel coordinates
        p_startx = startx * (dim_x0/_UTM_UNITS)
        p_stopx = stopx * (dim_x0/_UTM_UNITS)
        
        p_starty = starty * (dim_y0/_UTM_UNITS)
        p_stopy = stopy * (dim_y0/_UTM_UNITS)
        
        num_x = int(dim_x0/dim_x1)
        num_y = int(dim_y0/dim_y1)
    
        #Find corresponding cropped image
        i_start = int(p_startx/dim_x1) #image with the left boumd
        i_stop = int(p_stopx/dim_x1) #image with the right bound
        
        j_start = int(p_starty/dim_y1)  
        j_stop = int(p_stopy/dim_y1)
       
        #Disregard trees that lie in the left over image resulting from dividing
        #image by new dimensions
        if(i_stop >= num_x or i_start >= num_x or j_stop >= num_y or j_start >= num_y):
            continue
    
        #Disregard trees along border of cropped images
        #These trees have bounding boxes crossing into more than one image
        if(i_start != i_stop or j_start != j_stop):
            continue

        #Move origin so that the pixel value is in reference to 0,0 of cropped image      
        crop_x_start = p_startx - (i_stop*dim_x1)
        crop_x_stop = p_stopx - (i_stop*dim_x1)
        crop_y_start = p_starty - (j_stop*dim_y1)
        crop_y_stop = p_stopy - (j_stop*dim_y1)

        #Standardized midpoints and width/height used for yolo labels
        s_width = (crop_x_stop-crop_x_start)/dim_x1
        s_height = (crop_y_start-crop_y_stop)/dim_x1
        s_x_mid = (crop_x_start+crop_x_stop)/(2*dim_x1)
        s_y_mid = (crop_y_start+crop_y_stop)/(2*dim_y1)
        
        #Verify that computations are correct by drawing bounding boxes
        #Do not run on final data
        #img = Image.open('tree_crop/images/tree_' + str(i_stop) + '_' + str(j_stop) + '.jpg')
        #im_draw = ImageDraw.Draw(img)
        #im_draw.rectangle([crop_x_start, crop_y_stop, crop_x_stop, crop_y_start], width = 6, outline ="red")
        #img.save('tree_crop/images/tree_' + str(i_stop) + '_' + str(j_stop) + '.jpg')
        
        fileName = f"tree_crop/labels/{Path(impath).stem}_{i_stop}_{j_stop}.txt"
        txt = "0 {w_c:.8f} {h_c:.8f} {w:.8f} {h:.8f}\n"
        with open( fileName, 'a') as f:
            f.write(txt.format(w_c=s_x_mid, h_c=s_y_mid, w=s_width, h=s_height))
            #f.write(txt.format(w_c=p_startx, h_c=p_stopx, w=p_starty, h=p_stopy))

def select_train_valid_refactored(train, valid):
    processed_count = 0
    images = glob.glob("tree_crop/images/*.jpg")
    random.Random(4).shuffle(images)
    
    #Parse training set
    for image in images:
        imagePath = Path(image).stem
        stem = imagePath.stem
        if (processed_count < train):
            train_valid_folder = "train"
        else:
            train_valid_folder = "valid"
        if(os.path.exists(f'tree_crop/labels/{stem}.txt')):
            shutil.copy(imagePath, f'data/images/{train_valid_folder}/{imagePath.name}')
            shutil.copy(f'tree_crop/labels/{stem}.txt', 'data/labels/{train_valid_folder}/{stem}.txt')
            processed_count = processed_count + 1
        if (processed_count == train + valid):
            break;


