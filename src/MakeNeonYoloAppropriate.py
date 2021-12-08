# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:04:11 2021

@author: sparky
"""

import os
from pathlib import Path
import glob
import random
import csv
from PIL import Image


def generate_all_bounding_boxes_for_downloaded_tifs_as_list(site = ""):
    #[(site, (bounding box tuple))]
    bounding_boxes = get_all_bounding_boxes(site = "")
    tifList = get_image_list()
    for path in tifList:
        geosite = get_geosite_from_image_path(path)
        try:
            for box in bounding_boxes[geosite]:
                yield geosite, box
        except Exception:
            pass
        
    return result
def get_all_bounding_boxes_for_downloaded_tifs_as_list(site = ""):
    #[(site, (bounding box tuple))]
    result = []
    bounding_boxes = get_all_bounding_boxes(site = "")
    tifList = get_image_list()
    for path in tifList:
        geosite = get_geosite_from_image_path(path)
        try:
            for box in bounding_boxes[geosite]:
                result.append((geosite,box))
        except Exception:
            pass
        
    return result

def convert_all_tif_to_jpg_and_place(trainPath='data/images/train/', validPath='data/images/valid/'):
    images = get_image_list()
    for path in images:
        imRoot = path.split('.')[0].split('/')[-1] + ".jpg"
        print(imRoot)
        convert_tif_to_jpg(path, trainPath+imRoot)
        convert_tif_to_jpg(path, validPath+imRoot) 

def convert_tif_to_jpg(tifpath, jpgpath):
    Image.MAX_IMAGE_PIXELS = None
    with Image.open(tifpath) as im:
        im.save(jpgpath)

def get_geosite_from_image_path(image_path):
    pathcomponents = image_path.split('_')
    geo_index = pathcomponents[3] + "_" + pathcomponents[4]
    return geo_index

def get_site_from_image_path(image_path):
    pathcomponents = image_path.split('_')
    site = pathcomponents[1]
    return site;

def get_annotation_list_for_image(image_path):
    site = get_site_from_image_path(image_path)
    geo_index = get_geosite_from_image_path(image_path)
    primary_annotations = get_confidence_and_boxes(site)
    return primary_annotations[geo_index]


def get_annotation_list_for_geosite(geosite, site):
    primary_annotations = get_confidence_and_boxes(site)
    return primary_annotations[geosite]
    
    
def get_image_list(site=""):
    imageFileList = glob.glob(f'data/images/*{site.upper()}*.tif')
    return imageFileList
    
def get_all_bounding_boxes(site=""):
    #[{ key=geo_index, value =[tuple with confidence, and bounding box coordinates]}]
    result = {}
    csv_annotation = glob.glob(f'data/{site.upper()}*.csv')
    if len(csv_annotation) == 0:
        print("Lost file - updated")
        return
    for file in csv_annotation:
        with open(file, mode='r') as infile:
            reader = csv.reader(infile)
            next(reader)
            for row in reader:
                result.setdefault(row[10],[]) 
                result[row[10]] += [(float(row[1]), float(row[2]), float(row[3]), float(row[4]))]
    return result

def standardize_box_and_write_to_output_path(bounding_boxes, annotationOutputDir):
    #bounding_boxes = MakeNeonYoloAppropriate.consolidate_bounding_box_list_to_dictionary(train_boxes)
    for geosite, boxList in bounding_boxes:
        standardized_annotation = yolov5Annotation(geosite, boxList)
        fileBase = construct_file_base_from_geosite(geosite)
        annotationPath = Path(annotationOutputDir + fileBase+ '.txt')
        writeAnnotationToFile(boxList, annotationPath)


def consolidate_bounding_box_list_to_dictionary(data_list):
    result = {}
    for entry in data_list:
        for geosite, box in entry:
            result.setdefault(geosite, [])
            result[geosite] += [box]
    return result

def split_list_to_train_valid_test(data_list, train_proportion, valid_proportion, test_proportion, maximumTotalCount=None):
    if maximumTotalCount is None:
        maximumTotalCount = len(data_list)
    random.shuffle(data_list)
    assert (train_proportion + valid_proportion + test_proportion <= 1)
    true_max = maximumTotalCount if maximumTotalCount < len(data_list) else len(data_list)
    
    trainStart = 0
    trainEnd = int(train_proportion*true_max)
    validStart = trainEnd + 1 if trainStart != trainEnd else trainEnd
    validEnd = validStart + int(valid_proportion*true_max)
    testStart = validEnd + 1 if validStart != validEnd else validEnd
    testEnd = testStart + int(test_proportion*true_max)
    
    return data_list[trainStart:trainEnd], data_list[validStart:validEnd], data_list[testStart:testEnd]
    


def yolov5Annotation(geosite, row):
    geoX, geoY = map(int, geosite.split("_"))   
    
    result = []
    utm_units = 1000.0

    left = row[0] - geoX
    right = row[2] - geoX
    top = utm_units - (row[1] - geoY)
    bottom = utm_units - (row[3] - geoY)

    s_left = left/utm_units
    s_right = right/utm_units
    s_top = top/utm_units
    s_bottom = bottom/utm_units
    result += [( (s_left+s_right)/2,
            (s_top + s_bottom)/2,
            s_right - s_left,
            s_top - s_bottom)]
        
    return result

def construct_file_base_from_geosite(geosite):
    tifList = get_image_list()
    for filePath in tifList:
        if geosite in filePath:
            strippedExtension = filePath.split('.')[0]
            return strippedExtension.split('/')[-1]
        
def writeAnnotationToFile(row, outputPath):
    txt = "0 {w_c:.8f} {h_c:.8f} {w:.8f} {h:.8f}\n"
    with open(outputPath, 'a+') as f:
            f.write(txt.format(w_c=row[0], h_c=row[1], w=row[2], h=row[3]))

def setup_yolo_directories():
    #import os
    paths =[Path("data/images"),
            Path("data/images/train"),
            Path("data/images/valid"),
            Path("data/labels/train"),
            Path("data/labels/valid"),
            Path("download")
        ]
    for directory in paths:
        if not os.path.exists(directory):
            os.makedirs(directory)
            
