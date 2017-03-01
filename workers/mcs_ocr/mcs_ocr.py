
import requests
import json
import sys
import os

from celery import Celery
from celery.utils.log import get_task_logger

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from utils.get_image import get_image
from utils.decorators import unpack_chained_kwargs


API_ENDPOINT = 'http://localhost:5000/api/v1/download'
MCS_ENDPOINT = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/ocr'

DEBUG_OUTPUT = '../../_TestData/bgbill12/bgbill12.json'

DEBUG_OUTPUT_FOLDER = '_Output'

logger = get_task_logger(__name__)
app = Celery('mcs_ocr')
app.config_from_object('celeryconfig')


def _debug():
    debug_file_path = os.path.abspath(DEBUG_OUTPUT)
    with open(debug_file_path, 'rb') as fd:
         data = fd.read()

    return json.loads(data.decode("utf-8"))


@app.task(name='workers.mcs_ocr.mcs_ocr', queue='mcs_ocr')
@unpack_chained_kwargs
def mcs_ocr(*args, **kwargs):
    debug = kwargs.get('debug', 'False')
    logger.warn("Debug: {0}".format(debug))

    if debug:
        kwargs['mcs_data'] = _debug()
        return kwargs

    img_data = get_image(kwargs['user_token'], kwargs['doc_id'])

    uri = "{0}/{1}".format(API_ENDPOINT, kwargs['doc_id'])
    logger.info(uri)

    headers = {'Ocp-Apim-Subscription-Key': kwargs['mscs_vision_api_key'],
               'Content-Type': 'application/octet-stream'}

    try:
        r = requests.post(MCS_ENDPOINT, data=img_data, headers=headers)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return

    logger.info("{0} : {1}".format(r.status_code, r.reason))

    data = r.json()
    logger.debug(data)

    kwargs['mcs_data'] = data

    output_filename = "{0}.png".format(kwargs['doc_id'])
    output_filepath = os.path.abspath(os.path.join(DEBUG_OUTPUT_FOLDER, output_filename))
    output_filepath += '.json'

    if not os.path.isdir(os.path.join(DEBUG_OUTPUT_FOLDER)):
        os.mkdir(os.path.join(DEBUG_OUTPUT_FOLDER))

    print(output_filepath)
    with open(output_filepath, 'w+') as f:
        f.write(json.dumps(data))

    # Only return one value of type dict. Otherwise subsequent workers decorated with 'unpack_chained_kwargs' will fail.
    return kwargs
