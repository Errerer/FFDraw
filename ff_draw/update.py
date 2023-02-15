import logging
import os
import pathlib
import re

import requests

update_host = {
    'github': 'https://raw.githubusercontent.com/',
    'fastgit': 'https://raw.fastgit.org/',
}
update_uri = 'nyaoouo/FFDraw/master/version.txt'

logger = logging.getLogger('UpdateChecker')

update_desc = [
    'major',
    'feature',
    'bugfix'
]


def check(select_host='github'):
    try:
        is_latest, local_version = _check(select_host)
    except Exception as e:
        logger.error('check update fail, please check network connection or change update source', exc_info=e)


def _check(select_host='github'):
    remote_version = local_version = 0, 0, 0
    if (local_version_path := pathlib.Path(os.environ['ExcPath']) / 'version.txt').exists():
        if _match := re.match(r'^(\d+)\.(\d+)\.(\d+)$', local_version_path.read_text()):
            local_version = int(_match.group(1)), int(_match.group(2)), int(_match.group(3)),
    (res := requests.get(update_host[select_host] + update_uri)).raise_for_status()
    if _match := re.match(r'^(\d+)\.(\d+)\.(\d+)$', res.text):
        remote_version = int(_match.group(1)), int(_match.group(2)), int(_match.group(3)),
    logger.info(f'local version: {local_version}    remote version: {remote_version}')
    for l, r, d in zip(local_version, remote_version, update_desc):
        if r > l:
            logger.warning(f'there is a {d} update from {local_version} => {remote_version}')
            return False, local_version
        elif r < l:  # custom source?
            return True, local_version
    return True, local_version
