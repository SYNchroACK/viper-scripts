import requests
from os import listdir
from os.path import isfile, join, abspath
import hashlib
import re
import argparse

usage = "viperupload.py [-d DIRECTORY | -s SAMPLE] -t tags"
parser = argparse.ArgumentParser(description=usage)

parser.add_argument('-d','--directory',type=str, help='Directory to submit')
parser.add_argument('-s','--sample',type=str,help='Single sample to submit')
parser.add_argument('-t','--tags',type=str,help='Additional tags',nargs='+')
args = parser.parse_args()
dir = args.directory
sample = args.sample
tags = args.tags

if not(bool(dir)^bool(sample)):
	print 'Must provide either -s or -d options (not both)'
	exit()

global url_upload
global url_search
global url_tag
global url_run
#input location of your viper instance
url_upload = 'http://localhost:8080/file/add'
url_search = 'http://localhost:8080/file/find'
url_tag = 'http://localhost:8080/file/tags/add'
url_run = 'http://localhost:8080/modules/run'

def add_tags(filesha,tags):
	#this method will add all tags that should be added by default
	#imphash will be added in addition to user specified tags
	#imphash method
	params = {'sha256': filesha, 'cmdline': 'pe imphash'}
	r = requests.post(url_run,params)
	data = r.json()
	searchobj = re.search(r'Imphash\:\ \\x1b\[1m(.+?)\\x1b\[0m', data)
	if not searchobj is None:
		tags.append(searchobj.group(1))
	params = {'sha256': filesha, 'tags': ",".join(tags)}
	r = requests.post(url_tag, params)

def submit_sample(fullpath,tags):
	#do a quick search for the file so we don't add it multiple times
	#viper will de-dup multiple uploads, but this is unnecessary and 
	#could potentially cause overhead in the case of large upload sets
	filesha = hashlib.sha256(open(fullpath,'rb').read()).hexdigest()
	search = {'sha256': filesha}
	r = requests.post(url_search, search)
	data = r.json()
	if(len(data) > 0):
		#our sample is already in the DB, we'll just add the tags
		print("%s is already in the DB" % fullpath)
		add_tags(filesha,tags)
	else:
		#in this case, we add the sample and the tags
		print("%s added to DB")
		files = {'file': open(file, 'rb')}
		r = requests.post(url_upload, files=files)
		add_tags(filesha,tags)
		
if (dir):
	filelist = [ f for f in listdir(dir) if isfile(join(dir,f)) ]
	for file in filelist:
		fullpath = join(dir,file)
		submit_sample(fullpath,tags)

if (sample):
	if (isfile(sample)):
		fullpath = abspath(sample)
		submit_sample(fullpath,tags)
