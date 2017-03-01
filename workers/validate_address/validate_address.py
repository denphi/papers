import os
import requests
import json
import sys

from celery import Celery
from celery.utils.log import get_task_logger

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from utils.decorators import unpack_chained_kwargs


DEBUG_FIRSTNAME = u'John'
DEBUG_SURNAME = u'Stein'
DEBUG_POSTCODE_END = u'2RX'

logger = get_task_logger(__name__)
app = Celery('validate_address')
app.config_from_object('celeryconfig')


def get_address_scan(firstname, surname, postcode_end, mcs_data):
    logger.debug(firstname)
    logger.debug(surname)
    logger.debug(postcode_end)
    logger.debug(mcs_data)

    # regions = json.loads(mcs_data)
    # logger.debug(regions)

    address = u''
    capture = 0
    for region in mcs_data['regions']:
        for line in region['lines']:
            for word in line['words']:
                if word["text"].lower() == firstname.lower() or word[
                    "text"].lower() == surname.lower() and capture == 0:
                    capture = 1
                if capture == 1:
                    # logic below excludes name if at beginning of address
                    if not (address == u'' and (
                            word["text"].lower() == firstname.lower() or word["text"].lower() == surname.lower())):
                        address = address + word["text"] + u' '
                if word["text"].lower() == postcode_end.lower():
                    capture = 2
                if capture == 2:
                    break
            if capture == 2:
                break
        if capture == 2:
            break

    return address


@app.task(name='workers.validate_address.validate_address', queue='validate_address')
@unpack_chained_kwargs
def validate_address(*args, **kwargs):
    debug = kwargs.get('debug', 'False')
    logger.warn("Debug: {0}".format(debug))

    address = get_address_scan(DEBUG_FIRSTNAME,
                               DEBUG_SURNAME,
                               DEBUG_POSTCODE_END,
                               kwargs['mcs_data'])

    # Validate address
    logger.debug(address)
    url_addr = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {'address': address, 'key': kwargs['google_api_key']}
    res = requests.get(url_addr, params=payload)
    logger.debug(res.url)
    out = res.json()
    logger.debug(out)

    google_address = ''
    match = ''
    partial_match = False
    if len(out['results']):
        google_address = out['results'][0]['formatted_address']

        if out['results'][0].has_key('partial_match'):
            partial_match = out['results'][0]['partial_match']

    logger.info("{0} : {1}".format(google_address, partial_match))

    # return google_address, partial_match

    # Only return one value of type dict. Otherwise subsequent workers decorated with 'unpack_chained_kwargs' will fail.
    return kwargs
