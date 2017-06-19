#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import requests
import sys

import six.moves.urllib.request as ulib_request

github_api_base = 'https://api.github.com'
# https://developer.github.com/v3/repos/releases/


def wget(url, outfile):
    print('GRAB %s as %s' % (url, outfile))
    try:
        os.makedirs(os.path.dirname(outfile))
    except OSError as err:
        # OSError: [Errno 17] File exists:
        if err.errno != 17:
            raise
    if not os.access(outfile, os.F_OK):
        ulib_request.urlretrieve(url, outfile)
    else:
        print('Skipping [%s] already exists' % (outfile))


def is_available_already(outfile):
    req = requests.head('https://tarballs.openstack.org/%s' % (outfile))
    return req.status_code == 200


def main():
    for arg in sys.argv[1:]:
        try:
            project, release, pattern, mirror_path = arg.split(':', 4)
        except ValueError:
            print('Skipping malfomed arg: [%s]' % (arg), file=sys.stderr)
            continue

        pattern_re = re.compile(pattern)
        if release == '':
            release = 'latest'

        url = ('%s/repos/%s/releases/%s' % (github_api_base, project, release))
        req = requests.get(url)
        if req.status_code != 200:
            response = {}
        else:
            response = req.json()

        tag = response.get('name')
        for asset in response.get('assets', []):
            browser_download_url = asset.get('browser_download_url')
            if pattern_re.search(browser_download_url):
                dir_base = os.path.join('.', mirror_path, tag)
                file_path = os.path.join(dir_base, asset['name'])

                if not is_available_already(file_path[2:]):
                    wget(browser_download_url, file_path)
                else:
                    print('Skipping [%s] already exists on mirror' %
                          (file_path[2:]))

if __name__ == '__main__':
    sys.exit(main())
