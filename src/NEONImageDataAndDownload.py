from pathlib import Path
import socket
import requests
import requests.packages.urllib3.util.connection as urllib3_cn
from random import sample



# Some globals

NEON_PRODUCT_CODE = "DP3.30010.001"

#keeping this low until all the moving parts work (development phase)
DEFAULT_DOWNLOAD_COUNT = 5;
defaultPhotoDropPath = Path("data/raw")
defaultCSVDropPath = Path("data/raw")
API_BASE = 'https://data.neonscience.org/api/v0/'


def allowed_gai_family():
    return socket.AF_INET

urllib3_cn.allowed_gai_family = allowed_gai_family


# Get information about the image data set
def getProductInfo(neon_image_product_code):
    product_info_endpoint = f'products/{neon_image_product_code}'
    product_details = requests.get(API_BASE+product_info_endpoint)
    #print(product_details.content)
    return product_details.content

# Returns a list of dictionaries with the photo name and download URL
def getListOfSiteFilesForYear(dataEndpointWithParams):
    responseWithListOfSiteFiles = requests.get(API_BASE + dataEndpointWithParams)
    return responseWithListOfSiteFiles.json()['data']['files']

# downloads a single photo to the photoDropPath
def download_image(photoName, photoURL, photoDropPath = defaultPhotoDropPath):    
    photoRequest = requests.get(photoURL, allow_redirects=True)
    with open(Path(photoDropPath) / Path(photoName), 'wb') as f:
       f.write(photoRequest.content)

# downloads photos from the list of dictionaries returned from getListOfSiteFilesForYear
def download_images(image_dictionary, photoDropPath = defaultPhotoDropPath):
    for entry in image_dictionary:
        download_image(entry['name'], entry['url'], photoDropPath)


def download_n_images(dataEndpointWithParams, n = DEFAULT_DOWNLOAD_COUNT, photoTargetDirectory=defaultPhotoDropPath):
    #dataEndpointWithParams = f'data/{neon_image_product_code}/{site}/{year_month}?package=basic'
    image_list_dictionary = getListOfSiteFilesForYear(dataEndpointWithParams)
    count = n if n < len(image_list_dictionary) else len(image_list_dictionary)
    subset = sample(image_list_dictionary, n)
    download_images(subset, photoTargetDirectory)

def make_data_endpoint(site, year_month, neon_image_product_code=NEON_PRODUCT_CODE):
    return f'data/{neon_image_product_code}/{site}/{year_month}?package=basic'

