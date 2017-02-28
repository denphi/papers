#!/usr/bin/env python3

import requests
import argparse
import base64

API_URL = 'http://localhost:5000/api/v1/'


def header(msg, overline_char='=', underline_char='='):
    print(overline_char * 80)
    print(msg)
    print(underline_char * 80)


def _parse_args():
    desc = 'Uploads Base64 file'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('email',
                        help='email')
    parser.add_argument('password',
                        help='Password')
    parser.add_argument('file',
                        help='File')

    return parser.parse_args()


def login(email, password):
    header('Logging in...')
    login_url = API_URL + 'auth/login'
    headers = {'Content-Type': 'application/json'}
    payload={'email': email, 'password': password}
    response = requests.post(login_url,
                             json=payload,
                             headers=headers)
    print("{0} : {1}".format(response.status_code, response.reason))

    return response.json().get('token')


def upload(token, file_path):
    header('Uploading...')
    with open(file_path, 'rb') as fd:
         b64data = base64.b64encode(fd.read())

    upload_url = API_URL + 'upload'
    headers = {'Authorization': token,
               'Content-Type': 'application/json'}
    payload = {'image_data': b64data.decode("utf-8"),
               'site_name': 'Test',
               'url': 'http://www.test.com'}
    response = requests.post(upload_url, json=payload, headers=headers)
    print("{0} : {1}".format(response.status_code, response.reason))

    if response.status_code == 200:
        print(response.text)


def main():
    args = _parse_args()

    token = login(args.email, args.password)
    upload(token, args.file)


if __name__ == '__main__':
    main()
