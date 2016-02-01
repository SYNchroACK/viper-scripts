import requests
from os import listdir
from os.path import isfile, join, abspath
import hashlib
import re
import argparse
from optparse import OptionParser

'''
This is a modified version of pmelson's upload script, with CLI support
'''

usage = "viperupload.py [-d DIRECTORY | -s SAMPLE] -t tags"
opt_parser = OptionParser(usage=usage)

opt_parser.add_option("-d", "--directory", action="store",dest="directory",default=None,
  help="Directory to submit")
opt_parser.add_option("-s", "--sample", action="store",dest="sample",default=None,
  help="Single sample to submit")
opt_parser.add_option("-t", "--tags", action="store",type=float,dest="tags",default=None,
  help="Additional tags that the malware sample could use added")
(options, args) = opt_parser.parse_args()

if (options.directory ^ options.sample == 1):
   print 'Must provide either -d or -s options (not both)'
   exit()

url_upload = 'http://localhost:8080/file/add'
url_tag = 'http://localhost:8080/file/tags/add'
url_run = 'http://localhost:8080/modules/run'

if (options.directory):
  #expand the directory and store as filelist
  filelist = [ f for f in listdir(options.directory) if isfile(join(options.directory,f))) ]
  for file in filelist:
    fullpath = join(options.directory,file)
    files = {'file': open(fullpath, 'rb')}
    #upload the file
    r = requests.post(url_upload, files=files)
    filesha = hashlib.sha256(open(join(filepath,file)).read()).hexdigest()
    params = {'sha256': filesha, 'cmdline': 'pe impash'}
    #send the command
    r = requests.post(url_run,params)
    data = r.json()
    searchobj = re.search(r'Imphash\:\ \\x1b\[1m(.+?)\\x1b\[0m', data)
    imphash = searchobj.group(1) 
    print imphash
    if (options.tags is None):
      params = {'sha256': filesha, 'tags': imphash}
    else:
      params = {'sha256': filesha, 'tags': imphash + "," + options.tags}
    #send the request
    r = requests.post(url_tag, params)

if (options.sample):
  #for an individual sample,  i'll keep a lot the same logic as above
  if (isfile(options.sample)):
    fullpath = abspath(options.sample)
    files = {'file': open(fullpath, 'rb')}
    #upload the file
    r = requests.post(url_upload, files=files)
    filesha = hashlib.sha256(open(join(filepath,file)).read()).hexdigest()
    params = {'sha256': filesha, 'cmdline': 'pe impash'}
    #send the command
    r = requests.post(url_run,params)
    data = r.json()
    searchobj = re.search(r'Imphash\:\ \\x1b\[1m(.+?)\\x1b\[0m', data)
    imphash = searchobj.group(1)
    print imphash
    if (options.tags is None):
      params = {'sha256': filesha, 'tags': imphash}
    else:
      params = {'sha256': filesha, 'tags': imphash + "," + options.tags}
    #send the request
    r = requests.post(url_tag, params)
