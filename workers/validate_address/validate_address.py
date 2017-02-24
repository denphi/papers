import os
import requests
import json

from celery import Celery
from celery.utils.log import get_task_logger

DEBUG_FIRSTNAME = u'John'
DEBUG_SURNAME = u'Stein'
DEBUG_POSTCODE_END = u'2RX'

logger = get_task_logger(__name__)
app = Celery('validate_address', broker='pyamqp://guest@localhost//')

GOOGLE_API_KEY = 'AIzaSyBRpWc0C_DvxiGfaOu5fITfJgsqPWzevm0'

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
def validate_address(*args, **kwargs):
    logger.info(args[0])
    address = get_address_scan(DEBUG_FIRSTNAME,
                               DEBUG_SURNAME,
                               DEBUG_POSTCODE_END,
                               args[0][0][0]['mcs_data']) # FIX: arg get boxed with each call

    # Validate address
    logger.debug(address)
    url_addr = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {'address': address, 'key': 'AIzaSyBRpWc0C_DvxiGfaOu5fITfJgsqPWzevm0'}
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

    return args
