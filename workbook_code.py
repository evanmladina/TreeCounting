#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append('src/')

import TreeAnnotations
import NEONImageDataAndDownload
import MakeNeonYoloAppropriate
from path import Path


# In[2]:


# Some globals

site = "YELL"
year = "2019"
year_month = "2019-07"
geosite = ["535000_4971000"]

numberOfImagesToDownload = 1
train_proportion = 0.7
valid_proportion = 0.2
test_proportion = 0.1
maximumTotalCount = 5000

defaultDownloadPath = Path("download/")


# In[3]:


# preliminary directory setup
MakeNeonYoloAppropriate.setup_yolo_directories()


# In[6]:


# get CSV data
TreeAnnotations.downloadAnnotation(site, defaultDownloadPath/ f"{site.upper()}_{year}.csv")


# In[ ]:


#download images
imageListEndpoint = NEONImageDataAndDownload.make_data_endpoint(site, year_month)
NEONImageDataAndDownload.download_n_images(imageListEndpoint, numberOfImagesToDownload, defaultDownloadPath)


# In[]:


MakeNeonYoloAppropriate.convert_all_tif_to_jpg_and_place()


# In[6]:


# select training and validation annotations based on images downloaded
bounding_boxes = MakeNeonYoloAppropriate.get_all_bounding_boxes_for_downloaded_tifs_as_list()
train_boxes, valid_boxes, test_boxes = MakeNeonYoloAppropriate.split_list_to_train_valid_test(bounding_boxes, train_proportion, valid_proportion, test_proportion, maximumTotalCount)
MakeNeonYoloAppropriate.standardize_box_and_write_to_output_path(train_boxes, 'data/labels/train/')
MakeNeonYoloAppropriate.standardize_box_and_write_to_output_path(valid_boxes, 'data/labels/valid/')

