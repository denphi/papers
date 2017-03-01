
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


API_ENDPOINT = 'http://localhost:5000/api/v1/download'
MCS_ENDPOINT = 'http://localhost:5001/ocr/v3'

DEBUG_OUTPUT_FOLDER = '_Output'

logger = get_task_logger(__name__)
app = Celery('mcs_ocr_dotnet')
app.config_from_object('celeryconfig')


@app.task(name='workers.mcs_ocr_dotnet.mcs_ocr_dotnet', queue='mcs_ocr_dotnet')
def mcs_ocr_dotnet(*args, **kwargs):
    debug = kwargs.get('debug', 'False')
    logger.warn("Debug: {0}".format(debug))

    uri = "{0}/{1}".format(API_ENDPOINT, kwargs['doc_id'])
    logger.info(uri)

    headers = {'Content-Type': 'application/json'}

    try:
        r = requests.post(MCS_ENDPOINT, json={'url': uri}, headers=headers)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return

    logger.info("{0} : {1}".format(r.status_code, r.reason))

    data = r.json()
    logger.debug(data)

    data_dict = {'mcs_data': data}

    output_filename = "{0}.png".format(kwargs['doc_id'])
    output_filepath = os.path.abspath(os.path.join(DEBUG_OUTPUT_FOLDER, output_filename))
    output_filepath += '.json'

    if not os.path.isdir(os.path.join(DEBUG_OUTPUT_FOLDER)):
        os.mkdir(os.path.join(DEBUG_OUTPUT_FOLDER))

    print(output_filepath)
    with open(output_filepath, 'w+') as f:
        f.write(json.dumps(data))

    kwargs.update(data_dict)

    # Only return one value of type dict. Otherwise subsequent workers decorated with 'unpack_chained_kwargs' will fail.
    return kwargs
