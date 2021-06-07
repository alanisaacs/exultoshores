# FOR WSGI ON APACHE
#def application(environ, start_response):
#    status = '200 OK'
#    output = b'Hello'
#    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
#    start_response(status, response_headers)
#    return [output]

#activate_this = '/var/www/eos/wines/.venv/bin/activate_this.py'
#with open(activate_this) as file_:
#    exec(file_.read(), dict(__file__=activate_this))

#!/usr/bin/env python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/eos/')

from __init__ import app as application

# Secret key is set in /etc/apache2/envvars
#application.secret_key = 'KJyg7'
