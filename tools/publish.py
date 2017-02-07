#!/usr/bin/env python3

import logging
import os
import sys

from docutils.core import publish_string

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    input_file = os.getenv('SCRATCH_INPUT_FILE', 'scratch.rst')
    logging.debug('Input file: {}'.format(input_file))
    with open(input_file) as f:
        in_string = f.read()
        overrides = {
            # 'stylesheet':'css/plain.css',
        }
        html5 = publish_string(
            source=in_string,
            settings_overrides=overrides,
            writer_name='html5',
        )
        sys.stdout.write(html5.decode('UTF-8'))
