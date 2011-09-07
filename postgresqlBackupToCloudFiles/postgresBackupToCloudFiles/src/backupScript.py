#!/usr/bin/python

import cloudfiles
from myConfig import *
# myConfig should be a modified copy of configTemplate.py with your settings in it.
from datetime import datetime
import os


startime = datetime.now()

os.chdir(TMPDIR)
commandline = 'pg_dump -w -h localhost -U ' + DBUSER + ' -f ' + new.dump + ' ' + DBNAME#postgres -w BIVstats
backupResult = subprocess.check_output(commandline)


cloudFConnection = cloudfiles.Connection(CLOUDFILEUSER, CLOUDFILESAPIKEY, authurl=CLOUDFILESAUTHHOST)

if CLOUDFILEDESTINATIONCONTAINERADDMONTHANDYEAR:
    containerName = str(startime.year) + '-' + str(startime.month) + '-' + CLOUDFILEDESTINATIONCONTAINER
else:    
    containerName = CLOUDFILEDESTINATIONCONTAINER
try:
    containers = cloudFConnection.get_containers(containerName)
except cloudfiles.errors.NoSuchContainer:
    cloudFConnection.create_container('containerName')


    
    
print containers