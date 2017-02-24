
import codecs
import json
import math
import os

from PIL import Image, ImageDraw

import numpy
import cv2

from celery import Celery
from celery.utils.log import get_task_logger


DEBUG_IMAGE = '../../_TestData/Microsoft_computer-vision-api/bgbill12/bgbill12.png'

DEBUG_OUTPUT_FOLDER = '_Output'


logger = get_task_logger(__name__)
app = Celery('find_regions', broker='pyamqp://guest@localhost//')


@app.task(name='workers.find_regions.find_regions', queue='find_regions')
def find_regions(*args, **kwargs):
    lower_val = 0 # Lower black pixel
    upper_val = 128 # Upper white pixel

    # Load image
    img = Image.open(os.path.expanduser(DEBUG_IMAGE))

    # Crop image
    width = img.size[0]
    height = img.size[1]

    new_width = int(math.ceil(width * 0.50))
    new_height = int(math.ceil(height * 0.30))

    img = img.crop((0, 0, new_width, new_height))

    # Create numpy array of pixels
    pixels = numpy.array(img)

    # Change color space
    hsv = cv2.cvtColor(pixels, cv2.COLOR_BGR2HSV)
    # gray_image = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)

    # Filter out pixels in range
    lower_bound = numpy.array([0, 0, lower_val])
    upper_bound = numpy.array([255, 255, upper_val])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Apply Bitwise-AND Mask
    gray_pixels = cv2.bitwise_and(pixels, pixels, mask=mask)

    # Detect Edges
    edges = cv2.Canny(mask, 175, 320, apertureSize=3)

    # Detect Contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 10)) # 5 herizontal
    dilation = cv2.dilate(edges, kernel, iterations=2)

    im2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(pixels, contours, -1, (0,255,0), 3)

    if not os.path.exists(DEBUG_OUTPUT_FOLDER):
        os.makedirs(DEBUG_OUTPUT_FOLDER)

    for i in range(0, len(contours)):
        img_crop = Image.fromarray(pixels)

        # Crop image
        x,y,w,h = cv2.boundingRect(contours[i])
        img_crop_region = img_crop.crop((x, y, x+w, y+h))

        # Scale up x200
        img_crop_region_double = img_crop_region.resize((w * 2, h * 2), Image.ANTIALIAS)

        # Save region image
        output_filepath = os.path.join(DEBUG_OUTPUT_FOLDER, "region_{0:03d}.png".format(i))
        img_crop_region_double.save(output_filepath)

    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(pixels,(x,y),(x+w,y+h),(0,255,0),2)

    # Display image
    gray_img = Image.fromarray(pixels)
    # gray_img.show()

    output_filepath = os.path.abspath(os.path.join(DEBUG_OUTPUT_FOLDER, 'find_regions.png'))
    gray_img.save(output_filepath)

    args[0]['doc_id'] = output_filepath
    return args
