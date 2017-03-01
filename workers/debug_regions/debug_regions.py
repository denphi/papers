
import requests
import codecs
import sys
import os

from PIL import Image, ImageDraw
from collections import OrderedDict
from ast import literal_eval as make_tuple

from celery import Celery
from celery.utils.log import get_task_logger

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from utils.get_image import get_image
from utils.decorators import unpack_chained_kwargs


DEBUG_OUTPUT_FOLDER = '_Output'

logger = get_task_logger(__name__)
app = Celery('debug_regions')
app.config_from_object('celeryconfig')

def _calc_rect(rect_string):
        rect = make_tuple(rect_string)
        rect_list = list(rect)
        rect_list[2] += rect_list[0]
        rect_list[3] += rect_list[1]
        return tuple(rect_list)


@app.task(name='workers.debug_regions.debug_regions', queue='debug_regions')
@unpack_chained_kwargs
def debug_regions(*args, **kwargs):
    debug = kwargs.get('debug', 'False')
    logger.warn("Debug: {0}".format(debug))

    img_data = get_image(kwargs['user_token'], kwargs['doc_id'])
    img = Image.open(img_data)
    draw = ImageDraw.Draw(img)

    mcs_data = kwargs['mcs_data']

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

    output_filename = "{0}.png".format(kwargs['doc_id'])
    output_filepath = os.path.abspath(os.path.join(DEBUG_OUTPUT_FOLDER, output_filename))
    logger.info(os.path.abspath(output_filepath))

    logger.info(output_filepath)

    img.save(output_filepath)

    # Show
    # img.show()

    # Only return one value of type dict. Otherwise subsequent workers decorated with 'unpack_chained_kwargs' will fail.
    return kwargs
