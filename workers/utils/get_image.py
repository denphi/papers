
import requests
from io import BytesIO

from celery.utils.log import get_task_logger


API_ENDPOINT = 'http://localhost:5000/api/v1/download'


logger = get_task_logger(__name__)


def get_image(user_token, doc_id):
    uri = "{0}/{1}".format(API_ENDPOINT, doc_id)
    logger.info(uri)

    headers = {'Authorization': user_token,
               'Cache-Control': 'no-cache'}

    logger.info("curl -X GET -H 'Authorization: {0}' {1}".format(user_token, uri))

    r = requests.get(uri, headers=headers)
    logger.info(r.status_code)

    return BytesIO(r.content)
