
from distutils import log

log.warn('See the error message above.');

DEFAULT_VERSION = "4.0.1"
DEFAULT_URL = "https://pypi.python.org/packages/source/s/setuptools/"

try:
    ...
except (TypeError):
    # Gestionar tipo incorrecto
    ...
except (KeyboardInterrupt):
    # Gestionar interrrupción de usuario
    ...

finally:
	#
	


####
import urllib.request
urllib.request.urlopen("http://example.com/foo/bar").read();


import requests
r = requests.get("http://example.com/foo/bar")

>>> print r.status_code
>>> print r.headers
>>> print r.content

url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)

url = "http://localhost:8080"
data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)

import json
import urllib2
data = {
        'ids': [12, 3, 4, 5, 6 , ...]
    }
    ####urllib2.urlopen("http://abc.com/api/posts/create",urllib.urlencode(data))
req = urllib2.Request('http://example.com/api/posts/create')
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(data))



import urllib2
import json

def basic_authorization(user, password):
     s = user + ":" + password
     return "Basic " + s.encode("base64").rstrip()
 
def submit_pull_request(user, repo):
     auth = (settings.username, settings.password)
     url = 'https://api.github.com/repos/' + user + '/' + repo + '/pulls'
     params = {'title': 'My Title', 'body': 'My Boday'}
     req = urllib2.Request(url,
         headers = {
             "Authorization": basic_authorization(settings.username, settings.password),
             "Content-Type": "application/json",
             "Accept": "*/*",   
             "User-Agent": "Myapp/Gunio", 
         }, data = json.dumps(params))

f = urllib2.urlopen(req)



    """
    
    comentario d varias
    lineas
    y
    mas
    
    """


import os
import shutil
import sys
import tempfile
import zipfile
import optparse
import subprocess
import platform
import textwrap
import contextlib
def archive_context(filename):
    # extracting the archive
    tmpdir = tempfile.mkdtemp()
    log.warn('Extracting in %s', tmpdir)
    old_wd = os.getcwd()
    try:
        os.chdir(tmpdir)
        with ContextualZipFile(filename) as archive:
            archive.extractall()

        # going in the directory
        subdir = os.path.join(tmpdir, os.listdir(tmpdir)[0])
        os.chdir(subdir)
        log.warn('Now working in %s', subdir)
        yield

    finally:
        os.chdir(old_wd)
        shutil.rmtree(tmpdir)


"""

Para boton

"""
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(6, GPIO.IN)

try:
    while True:
        if (not GPIO.input(6)):
            print ("LED encendido")
            GPIO.output(12,GPIO.HIGH)
            time.sleep(1)
            print ("LED apagado")
            GPIO.output(12, GPIO.LOW)
finally:
    GPIO.output(12, GPIO.LOW) # por seguridad
    print ("Haciendo limpieza")
    GPIO.cleanup()
    print ("Hasta luego")
