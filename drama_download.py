# coding: utf8

import sys
import logging
import json
import re
import argparse
import ConfigParser
import requests
import sched
import time
from datetime import datetime
from lxml import html
from baidupcsapi import PCS
from cloudsight import recognize_img


_CONF_FILE = 'config.ini'
logger = logging.getLogger('drama_downloader')
logger.setLevel(logging.INFO)


def _parse_conf(conf_file):
    try:
        conf = ConfigParser.SafeConfigParser()
        conf.read(conf_file)
        return conf
    except:
        logger.error('Failed to open conf file(%s).', _CONF_FILE)
        sys.exit(-1)


def _baidupan_login(conf):
    def _captcha_callback(img):
        logger.info('Try to recognize captcha...')
        result = recognize_img(img)
        if not result:
            return ''

        m = re.search(r'\d+', result)
        if m:
            return m.group()

        return ''

    try:
        username = conf.get('baidupan', 'username')
        password = conf.get('baidupan', 'password')
        if not username or not password:
            logger.error('No username or password found.')
            return

        pcs = PCS(username,
                  password,
                  captcha_callback=_captcha_callback)

        logger.info('Baidupan login successfully.')

        return pcs
    except:
        import traceback
        traceback.print_exc()
        logger.error('Failed to login in baidupan.')


def download_drama(conf):
    pcs = _baidupan_login(conf)
    if not pcs:
        sys.exit(-1)

    for key, value in conf.items('drama'):
        url, day, rule = map(lambda x: x.strip(), value.split(';'))
        if not url or not rule:
            logger.error('Url or rule not found. (key=%s)', key)
            continue

        day = int(day)
        if day <= 0 or day + 1 != datetime.today().weekday():
            continue

        try:
            r = requests.get(url)
            if not r.ok:
                logger.error('Failed to fetch %s', url)
                continue

            tree = html.fromstring(r.text)
            resource_url = tree.xpath(rule)
            if not resource_url:
                logger.error('No resource found. (key=%s)', key)
                continue

            # TODO: save history to avoid duplicate
            pcs.add_download_task(resource_url,
                                  '%s/%s/' % (conf.get('baidupan', 'dest_dir'),
                                              key))
            if not r.ok:
                logger.error('Failed to add download task. (key=%s, url=%s)',
                             key, resource_url)
                continue

            logger.info('Add download task successfully. (key=%s, url=%s)',
                        key, resource_url)

        except Exception as e:
            logger.error('Error: %s', e.message)


def _parse_args():
    parser = argparse.ArgumentParser(description="Drama downloader")

    parser.add_argument('-d', dest='daemon', action='store_true', help='Daemon mode.')
    parser.add_argument('-c', dest='config', default=_CONF_FILE, help="Config file. Default is %s" % _CONF_FILE)

    return parser.parse_args()


_schedule = sched.scheduler(time.time, time.sleep)


if __name__ == '__main__':
    args = _parse_args()
    conf = _parse_conf(args.config)

    if not args.daemon:
        download_drama(conf)
        sys.exit(0)

    _schedule.enter(24 * 3600, 1, download_drama, (conf, ))
    logger.info('Drama downloader is running ...')
    _schedule.run()
