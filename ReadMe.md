A. Basic:
1. sudo apt install python
2. sudo apt install python-dev
3. sudo apt install python-pip

B. GDAL:
4. pip install numpy
5. pip install scipy
6. pip install pipenv
7. sudo add-apt-repository ppa:ubuntugis/ppa
8. sudo apt update
9. sudo apt install gdal-bin python-gdal
10 verify:
	a. open python shell
	b. import osgeo.gdal
	c. osgeo.gdal.VersionInfo()
	d. osgeo.gdal.__version__

C. Apache2:
11. sudo apt install apache2
12. sudo ufw enable
13. sudo ufw app list
14. sudo ufw allow 'Apache'
15. sudo ufw status
16. sudo systemctl status apache2
17. http://localhost

D. GRASS:
18. sudo apt install grass

19. sudo nano ~/.bashrc

20. add following lines:
export GISBASE="/usr/lib/grass74"
export PATH="$PATH:$GISBASE/bin:$GISBASE/scripts:$GISBASE/lib"
export PYTHONPATH="${PYTHONPATH}:$GISBASE/etc/python/"
export PYTHONPATH="${PYTHONPATH}:$GISBASE/etc/python/grass"
export PYTHONPATH="${PYTHONPATH}:$GISBASE/etc/python/grass/script"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$GISBASE/lib"
export GIS_LOCK=$$ 
export GISRC="$HOME/.grassrc7"

21. source ~/.bashrc


E. mod-wsgi:

22. sudo apt-get install libapache2-mod-wsgi
23. sudo a2enmod wsgi
24. sudo systemctl restart apache2
25. sudo nano /etc/apache2/conf-available/wsgi.conf :-
 	WSGIScriptAlias /test_wsgi /var/www/html/test_wsgi.py


26. sudo nano  /var/www/html/test_wsgi.py :-
def application(environ,start_response):
    status = '200 OK'
    html = '<html>\n' \
           '<body>\n' \
           '<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">\n' \
           'mod_wsgi Test Page\n' \
           '</div>\n' \
           '</body>\n' \
           '</html>\n'
    response_header = [('Content-type','text/html')]
    start_response(status,response_header)
    return [html]

27. sudo a2enconf wsgi
28. sudo systemctl restart apache2
29. http://localhost/test_wsgi


F. pywps:

30. pip install pywps

31. sudo nano /etc/apache2/sites-available/pywps.conf

32. add the following lines:

WSGIDaemonProcess pywps home=/var/www/html/wsgi user=www-data group=www-data processes=2 threads=5
WSGIScriptAlias /pywps /var/www/html/wsgi/pywps.wsgi process-group=pywps

<Directory /var/www/html/wsgi/>
    WSGIScriptReloading On
    WSGIProcessGroup pywps
    WSGIApplicationGroup %{GLOBAL}
    Require all granted
</Directory>

33. sudo nano /var/www/html/wsgi/pywps.wsgi

34. add the following lines:

#!/usr/bin/python2

from pywps.app.Service import Service
import sys
import os

sys.path.append("/var/www/html/")


from processes.sayhello import SayHello

processes = [
    SayHello()
]

application = Service(
    processes,
    ['pywps.cfg']
)


35. sudo nano /var/www/html/pywps.cfg


36. add the following lines:

[server]
maxsingleinputsize=1mb
maxrequestsize=3mb
url=http://localhost:80/pywps
outputurl=http://localhost:80/outputs/
outputpath=outputs
workdir=workdir
maxprocesses=10
parallelprocesses=2

[processing]
mode=default

[logging]
level=INFO
file=logs/pywps.log
database=sqlite:///logs/pywps-logs.sqlite3

[grass]
gisbase=/usr/lib/grass74/


37. sudo nano /var/www/html/processes/sayhello.py

38. add the following lines:

from pywps import Process, LiteralInput, LiteralOutput, UOM

class SayHello(Process):
    def __init__(self):
        inputs = [LiteralInput('name', 'Input name', data_type='string')]
        outputs = [LiteralOutput('response',
                                 'Output response', data_type='string')]

        super(SayHello, self).__init__(
            self._handler,
            identifier='say_hello',
            title='Process Say Hello',
            abstract='Returns a literal string output\
             with Hello plus the inputed name',
            version='1.3.3.7',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        response.outputs['response'].data = 'Hello ' + \
            request.inputs['name'][0].data
        response.outputs['response'].uom = UOM('unity')
        return response

39. sudo nano /var/www/html/processes/__init__.py


40. sudo nano /var/www/html/logs/pywps.log



41. sudo mkdir /var/www/html/outputs

42. sudo mkdir /var/www/html/workdir

43. sudo chmod -R 777 /var/www/

44. sudo a2ensite pywps

45. sudo systemctl restart apache2

 
G. set proper permissions to /var/www:

46. sudo chgrp www-data /var/www
47. sudo chmod 775 /var/www
48. sudo chmod g+s /var/www
49. sudo usermod -a -G www-data [YOURUSERNAME]
















