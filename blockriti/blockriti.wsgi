#!/usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/srv/www/blockriti/")
activate_this = '/srv/www/env/bin/activate_this.py'
with open ( activate_this ) as file_ :
        exec ( file_.read (), dict ( __file__=activate_this ))
from app import app as application

