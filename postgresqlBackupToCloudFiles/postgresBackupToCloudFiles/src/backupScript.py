#!/usr/bin/python


#    This is a simple program to backup from a PostgreSQL database to
#    Rackspace's Cloud Files
#    Copyright (C) 2011  Human Friendly Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


importfailed = False
try:
    import cloudfiles
except:
    print """You need to install the python-cloudfiles library from Rackspace"""
    importfailed = True
try:
    from myConfig import *
except:
    print """Copy the configTemplate.py file to myConfig.py and set all items 
    according to your settings.  Make sure the file is in the same folder as the
    backupScript.py or otherwise on your PYTHONPATH"""
    importfailed = True
# myConfig should be a modified copy of configTemplate.py with your settings in it.

try:
    from datetime import datetime
    import os
    import subprocess
    from subprocess import CalledProcessError
except:
    print """Standard library import error.  Check that you have Python 2.7 or 
    later and that the PYTHONPATH is properly configured."""
    importfailed = True

if importfailed:
    exit()

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
