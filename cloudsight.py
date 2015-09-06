# coding: utf8

import sys
import time
import requests
import logging


logger = logging.getLogger('cloudsight')
_RETRY_MAX = 10


def recognize_img(imgdata, file_name='code.jpg'):
    api_url = 'http://api.cloudsightapi.com/image_requests'
    res_url = 'http://api.cloudsightapi.com/image_responses/'
    headers = {
        'Origin': 'http://cloudsightapi.com',
        'HOST': 'api.cloudsightapi.com',
        'Authorization': 'CloudSight amZd_zG32VK-AoSz05JLIA',
    }
    post_data = {
        'image_request[locale]': 'en-US',
        'image_request[language]': 'en-US',
    }
    files = {
        'image_request[image]': (file_name, imgdata),
    }

    token_req = requests.post(api_url, data=post_data, headers=headers, files=files)
    token = token_req.json().get('token')
    if not token:
        logger.error('Failed to upload file')
        return

    count = 0
    while count < _RETRY_MAX:
        try:
            count += 1
            result = requests.get('%s%s'%(res_url, token), headers=headers)
            status = result.json()['status']
            if status == 'completed':
                return result.json()['name']
        except Exception, e:
            logger.error('Failed to get image recognize result.')
