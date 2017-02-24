
import requests
import codecs
import json
import os

from io import BytesIO
from PIL import Image, ImageDraw
from collections import OrderedDict
from ast import literal_eval as make_tuple

from celery import Celery
from celery.utils.log import get_task_logger

API_ENDPOINT = 'http://localhost:5000/api/v1/download'

DEBUG_OUTPUT_FOLDER = '_Output'

logger = get_task_logger(__name__)
app = Celery('debug_regions', broker='pyamqp://guest@localhost//')

def _calc_rect(rect_string):
        rect = make_tuple(rect_string)
        rect_list = list(rect)
        rect_list[2] += rect_list[0]
        rect_list[3] += rect_list[1]
        return tuple(rect_list)


def _get_image(user_token, doc_id):
    uri = "{0}/{1}".format(API_ENDPOINT, doc_id)
    logger.info(uri)

    headers = {'Authorization': user_token,
               'Cache-Control': 'no-cache'}

    logger.info("curl -X GET -H 'Authorization: {0}' {1}".format(user_token, uri))

    r = requests.get(uri, headers=headers)
    logger.info(r.status_code)

    return BytesIO(r.content)


@app.task(name='workers.debug_regions.debug_regions', queue='debug_regions')
def debug_regions(*args, **kwargs):

    img_data = _get_image(args[0][0]['user_token'], args[0][0]['doc_id'])
    img = Image.open(img_data)
    draw = ImageDraw.Draw(img)

    mcs_data = args[0][0]['mcs_data'] # FIX: arg get boxed with each call

    for region in mcs_data['regions']:
        rect = _calc_rect(region['boundingBox'])
        draw.rectangle(rect, outline='red')

        for line in region['lines']:
            rect = _calc_rect(line['boundingBox'])
            draw.rectangle(rect, outline='green')

            for word in line['words']:
                rect = _calc_rect(word['boundingBox'])
                draw.rectangle(rect, outline='blue')

    # Save
    if not os.path.exists(DEBUG_OUTPUT_FOLDER):
        os.makedirs(DEBUG_OUTPUT_FOLDER)

    output_filename = "{0}.png".format(args[0][0]['doc_id'])
    output_filepath = os.path.abspath(os.path.join(DEBUG_OUTPUT_FOLDER, output_filename))
    logger.info(os.path.abspath(output_filepath))

    logger.info(output_filepath)

    img.save(output_filepath)

    # Show
    # img.show()

    return args
