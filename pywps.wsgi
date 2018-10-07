#!/usr/bin/python2

from pywps.app.Service import Service
import sys
import os

sys.path.append("/var/www/html/")

# processes need to be installed in PYTHON_PATH
from processes.sayhello import SayHello

processes = [
    SayHello()
]

application = Service(
    processes,
    ['pywps.cfg']
)
