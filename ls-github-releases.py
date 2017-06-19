#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import requests
import sys

github_api_base = 'https://api.github.com'


def main():
    for project in sys.argv[1:]:
        url = ('%s/repos/%s/releases' % (github_api_base, project))
        req = requests.get(url)
        if req.status_code != 200:
            response = []
        else:
            response = req.json()

        for release in response:
            for asset in release.get('assets', []):
                tag = release.get('name')
                _id = release.get('id')
                browser_download_url = asset.get('browser_download_url')

                print('%s:%s:%s' % (tag, _id, browser_download_url))

if __name__ == '__main__':
    sys.exit(main())
