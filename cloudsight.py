# coding: utf8

import requests
import logging


logging.basicConfig()
logger = logging.getLogger('cloudsight')


_RETRY_MAX = 10
_REQ_URL = 'http://cloudsightapi.com/image_requests'
_CHECK_URL = 'http://cloudsightapi.com/image_responses/'
_HEADERS = {
    'Origin': 'http://cloudsightapi.com',
    'HOST': 'cloudsightapi.com',
    'Referer': 'http://cloudsightapi.com/api',
}


def _send_request(post_data, **kwargs):
    token_req = requests.post(_REQ_URL, data=post_data, headers=_HEADERS, **kwargs)
    token_data = token_req.json()
    token = token_data.get('token')
    if not token:
        logger.error('Failed to upload file (%s)' % token_data.get('error', ''))
        return

    count = 0
    while count < _RETRY_MAX:
        try:
            count += 1
            result = requests.get('%s%s' % (_CHECK_URL, token), headers=_HEADERS)
            result_data = result.json()
            status = result_data['status']
            if status == 'completed':
                return result_data['name']
        except Exception:
            logger.error('Failed to get image recognize result.')


def recognize_img_file(imgdata, file_name='code.jpg'):
    post_data = {
        'image_request[locale]': 'en-US',
        'image_request[language]': 'en-US',
    }

    files = {
        'image_request[image]': (file_name, imgdata),
    }

    return _send_request(post_data, files=files)


def recognize_img_url(img_url):
    post_data = {
        'image_request[locale]': 'en-US',
        'image_request[language]': 'en-US',
        'image_request[remote_image_url]': img_url
    }
    return _send_request(post_data)
