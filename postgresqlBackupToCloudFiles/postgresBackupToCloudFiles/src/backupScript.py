#!/usr/bin/python

import cloudfiles
from myConfig import *
# myConfig should be a modified copy of configTemplate.py with your settings in it.
from datetime import datetime
import os
import subprocess
from subprocess import CalledProcessError



startime = datetime.now()

os.chdir(TMPDIR)
#commandline = ['/usr/bin/pg_dump', '-w', '-h localhost', '-U' , DBUSER,
#               ' -f tmp.dump ', DBNAME]#postgres -w BIVstats
commandline = ['pg_dump', '-w', '-h', 'localhost', '-U', DBUSER, '-f',
               'tmp.dump', DBNAME]

print commandline
try:
    backupResult =  subprocess.check_output(commandline,
                                            stderr=subprocess.STDOUT)
except CalledProcessError as e:
    print e
    print e.output
    exit()
print backupResult

cloudFConnection = cloudfiles.Connection(CLOUDFILEUSER, CLOUDFILESAPIKEY, 
                                         authurl=CLOUDFILESAUTHHOST)

if CLOUDFILEDESTINATIONCONTAINERADDMONTHANDYEAR:
    containerName = str(startime.year) + '-' + str(startime.month) + '-' 
    containerName = containerName + CLOUDFILEDESTINATIONCONTAINER
else:    
    containerName = CLOUDFILEDESTINATIONCONTAINER
try:
    container = cloudFConnection.get_container(containerName)
except cloudfiles.errors.NoSuchContainer:
    container = cloudFConnection.create_container(containerName)

filesavename = str(startime.year) + str(startime.month) + str(startime.day) 
filesavename = filesavename + DBNAME + '-backup.dump'

remoteObjust = container.create_object(filesavename)
remoteObjust.load_from_filename('tmp.dump', verify=True)
