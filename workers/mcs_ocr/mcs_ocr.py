
import requests
import json
import os

from io import StringIO
from celery import Celery
from celery.utils.log import get_task_logger

API_ENDPOINT = 'http://localhost:5000/api/v1/download'

DEBUG_ENDPOINT = 'http://10.44.4.244:5000/ocr/v3'
DEBUG_JSON = '{"url": "http://favim.com/orig/201105/28/hate-life-people-simple-text-typography-Favim.com-57610.jpg"}'

DEBUG_OUTPUT_FOLDER = '_Output'

logger = get_task_logger(__name__)
app = Celery('mcd_ocr', broker='pyamqp://guest@localhost//')


def _get_image(user_token, doc_id):
    uri = "{0}/{1}".format(API_ENDPOINT, doc_id)
    logger.info(uri)

    headers = {'Authorization': user_token,
               'Cache-Control': 'no-cache'}

    logger.info("curl -X GET -H 'Authorization: {0}' {1}".format(user_token, uri))

    r = requests.get(uri, headers=headers)
    logger.info(r.status_code)

    return StringIO(r.content)


@app.task(name='workers.mcd_ocr.mcd_ocr', queue='mcs_ocr')
def mcs_ocr(*args, **kwargs):
    img_data = _get_image(args[0]['user_token'], args[0]['doc_id']) # FIX: arg get boxed with each call

    headers = {'Content-Type': 'application/json'}
    r = requests.post(DEBUG_ENDPOINT, data=DEBUG_JSON, headers=headers)
    logger.info(r.status_code)

    data = r.json()
    logger.debug(data)

    data_dict = {'mcs_data': data}
    args[0].update(data_dict)
    return args
