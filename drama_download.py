# coding: utf8

import sys
import logging
import json
import re
import pickle
import os
import argparse
import ConfigParser
import requests
import sched
import time
from datetime import datetime, date
from lxml import html
from baidupcsapi import PCS
from baidupcsapi.api import LoginFailed
from cloudsight import recognize_img
from const import _CONF_FILE, _LOG_FILE, _CODE_FILE, _SUPPORT_SITES


# fix problem for pyinstaller
# https://github.com/kennethreitz/requests/issues/557
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'cacert.pem'
)


_pcs = None
_history = {}

logging.basicConfig()
logger = logging.getLogger('drama_downloader')
logger.setLevel(logging.INFO)


def _parse_conf(conf_file):
    try:
        conf = ConfigParser.SafeConfigParser()
        if not os.path.exists(conf_file):
            logger.error('No config file found.')
            sys.exit(-1)

        conf.read(conf_file)
        return conf
    except:
        logger.error('Failed to open config file(%s).', conf_file)
        sys.exit(-1)


def _recognize_img(img):
    logger.info('Try to recognize captcha...')
    result = recognize_img(img)
    if not result:
        return ''

    m = re.search(r'\d+', result)
    if m:
        return m.group()

    return ''


def _get_pcs(conf):
    def _captcha_callback(img):
        code = _recognize_img(img)
        if code:
            return code

        with open(_CODE_FILE, 'wb') as f:
            f.write(img)

        logger.info('Code is saved to %s. Please enter captcha code.' % _CODE_FILE)
        return raw_input('captcha> ')


    global _pcs
    if _pcs:
        return _pcs

    try:
        username = conf.get('baidupan', 'username')
        password = conf.get('baidupan', 'password')
        if not username or not password:
            logger.error('No username or password found.')
            sys.exit(-1)

        _pcs = PCS(username,
                  password,
                  captcha_callback=_captcha_callback)

        logger.info('Baidupan login successfully.')

        return _pcs
    except LoginFailed:
        import traceback
        traceback.print_exc()
        logger.error('Failed to login in baidupan.')
        sys.exit(-1)


def _get_rule(url):
    for name, value in _SUPPORT_SITES.items():
        if url.startswith(name):
            return value


def download_drama(args):
    logger.info('Begin to download drama...')

    conf = _parse_conf(args.config)

    _load_history()

    for name, drama_url in conf.items('drama'):
        drama_url = drama_url.strip()
        if not drama_url:
            logger.error('Drama url must be given. (name=%s)', name)
            continue

        # get drama parse rule
        rule = _get_rule(drama_url)
        if not rule:
            logger.error('Unsupported site: %s.\nSupported sites:%s', drama_url, _SUPPORT_SITES.keys())
            continue

        try:
            # fetch content from drama url
            r = requests.get(drama_url)
            if not r.ok:
                logger.error('Failed to fetch %s', drama_url)
                continue

            # parse drama download url
            tree = html.fromstring(r.text)
            resource_url = tree.xpath(rule)
            if not resource_url:
                logger.error('No resource found. (name=%s)', name)
                continue

            resource_url = str(resource_url[0])

            download_history = _get_history(name)
            # check download history
            if download_history is not None and \
               download_history['url'] == resource_url:
                continue

            # add download task in baidupan
            pcs = _get_pcs(conf)
            pcs.add_download_task(resource_url,
                                  '%s/%s/' % (conf.get('baidupan', 'dest_dir'),
                                              name))
            if not r.ok:
                logger.error('Failed to add download task. (name=%s, url=%s)',
                             name, resource_url)
                continue

            # save download history
            _set_history(name, resource_url)
            logger.info('Add download task successfully. (name=%s, url=%s)',
                        name, resource_url)

        except Exception as e:
            logger.error('Error: %s', e.message)
            raise

    if args.daemon:
        _schedule.enter(24 * 3600, 0, download_drama, (args, ))


def _set_history(key, url):
    _history[key] = {
        'url': str(url),
    }

    _save_history()


def _get_history(key):
    return _history.get(key)


def _save_history():
    with open(_LOG_FILE, 'wb') as f:
        pickle.dump(_history, f)


def _load_history():
    if not os.path.exists(_LOG_FILE):
        return False

    global _history
    with open(_LOG_FILE, 'rb') as f:
        _history = pickle.load(f)

    return True


def _parse_args():
    parser = argparse.ArgumentParser(description="Drama downloader")

    parser.add_argument('-d', dest='daemon', action='store_true', help='Daemon mode.')
    parser.add_argument('-c', dest='config', default=_CONF_FILE, help="Config file. Default is %s" % _CONF_FILE)

    return parser.parse_args()


_schedule = sched.scheduler(time.time, time.sleep)


if __name__ == '__main__':
    args = _parse_args()

    if not args.daemon:
        download_drama(args)
        sys.exit(0)

    logger.info('Drama downloader is running ...')
    _schedule.enter(1, 0, download_drama, (args, ))
    _schedule.run()
