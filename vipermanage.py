import requests
from os import listdir, makedirs
from os.path import isfile, join, abspath, isdir
import hashlib
import re
import argparse
import pprint
import urllib2

#Global vars - Modify for your Viper use
global url_upload
global url_search
global url_tag
global url_run
global url_delete
global url_findtag
global url_download
url_upload = 'http://localhost:8080/file/add'    #add a sample
url_search = 'http://localhost:8080/file/find'   #find a sample
url_tag = 'http://localhost:8080/file/tags/add'  #add a tag
url_run = 'http://localhost:8080/modules/run'    #run a command
url_delete = 'http://localhost:8080/file/delete' #delete a sample
url_findtag = 'http://localhost:8080/tags/list'  #list all tags
url_download = 'http://localhost:8080/file/get'  #retrieve a file 

#functions
def add_tags(filesha,tags):
	#this method will add all tags that should be added by default
	#imphash will be added in addition to user specified tags
	#imphash method
	params = {'sha256': filesha, 'cmdline': 'pe imphash'}
	r = requests.post(url_run,params)
	data = r.json()
	searchobj = re.search(r'Imphash\:\ \\x1b\[1m(.+?)\\x1b\[0m', data)
	params = {'sha256': filesha, 'tags': ",".join(tags[0]) }
	if not searchobj is None:
		imphash = searchobj.group(1)
		params['tags'] += ",%s" % imphash
	r = requests.post(url_tag, params)

def submit_sample(fullpath,tags):
	#do a quick search for the file so we don't add it multiple times
	#viper will de-dup multiple uploads, but this is unnecessary and 
	#could potentially cause overhead in the case of large upload sets
	filesha = hashlib.sha256(open(fullpath,'rb').read()).hexdigest()
	search = {'sha256': filesha}
	r = requests.post(url_search, search)
	data = r.json()
	if('default' in data):
		#our sample is already in the DB, we'll just add the tags
		print("%s is already in the DB" % fullpath)
		add_tags(filesha,tags)
	else:
		#in this case, we add the sample and the tags
		print("%s added to DB" % fullpath)
		files = {'file': open(fullpath, 'rb')}
		r = requests.post(url_upload, files=files)
		add_tags(filesha,tags)

def mkdirs_p(path, is_dir=True):
	if not is_dir:
		path = os.path.split(path)[0]
	if path != '':
		import errno
		try:
			makedirs(path)
			return True
		except OSError as e:
			if e.errno == errno.EEXIST and isdir(path):
				return False
			else:
				raise
		except Exception as e:
			raise
		return False

if __name__ == '__main__':
	#Parsing options
	cli = argparse.ArgumentParser(description='Tool to create / modify / delete Portal users')
	group1 = cli.add_mutually_exclusive_group(required=True)
	group1.add_argument('-u', '--upload',  action='store_true', help="Upload Sample(s)")
	group1.add_argument('-d', '--download',action='store_true', help="Download Sample(s)")
	group1.add_argument('-l', '--list',    action='store_true', help="List Sample(s)")
	group1.add_argument('-r', '--remove',  action='store_true', help="Remove Sample(s)")
	cli.add_argument('-s','--sample',type=str, required=False, help="Single Sample")
	cli.add_argument('-S','--search',type=str, required=False, help="Search for sample (SHA256)")
	cli.add_argument('-t','--tags',  type=str, required=False, help="Tags to search on or add", nargs='+', action='append')
	cli.add_argument('-D','--dir',   type=str, required=False, help="Directory to upload or Dest Directory for Download")
	args = cli.parse_args()

	#Upload File
	if args.upload:
		if args.dir:
			filelist = [ f for f in listdir(args.dir) if isfile(join(args.dir,f)) ]
			for sample in filelist:
				fullpath = join(args.dir,sample)
				submit_sample(fullpath,args.tags)
		if (args.sample):
			if (isfile(args.sample)):
				fullpath = abspath(args.sample)
				submit_sample(fullpath,args.tags)
	#Download File
	if args.download:
		if args.search:
			#find the single sample and download it
			search = args.search
			mkdirs_p("downloads")
			destination_file = "./downloads/%s" % search
			print "downloads/%s - Downloading" % item['sha256']
			r =  urllib2.urlopen(url_download+"/"+search)
			with open(destination_file, "wb") as local_file:
				local_file.write(r.read())
			local_file.close()
		if args.tags:
			#do a find of all the files that match a tag and download them
			search = {'tag': args.tags[0]}
			r = requests.post(url_search, search)
			if "default" in items:
				mkdirs_p("downloads")
				for item in items['default']:
					print "downloads/%s - Downloading" % item['sha256']
					r =  urllib2.urlopen(url_download+"/"+item['sha256'])
					with open(destination_file, "wb") as local_file:
						local_file.write(r.read())
					local_file.close()	
	#List File
	if args.list:
		if args.search:
			#print out information about a particular sample
			#there isn't too much logic in this function
			#so we'll just leave it as is and not abstract it out
			search = {'sha256': args.search}
			r = requests.post(url_search, search)
			pp = pprint.PrettyPrinter(depth=6)
			pp.pprint(r.json())
		if args.tags:
			#print out information about samples that match the tags
			search = {'tag': args.tags[0]}
			r = requests.post(url_search, search)
			pp = pprint.PrettyPrinter(depth=6)
			pp.pprint(r.json())

	#Remove File
	if args.remove:
		if args.search:
			#find the single sample and remove it
			search = args.search
			r = urllib2.urlopen(url_delete+"/"+search)
			print("%s - removing" % item['sha256'])

		if args.tags:
			#find samples with that match a tag and remove them
			search = {'tag': args.tags[0]}
			r = requests.post(url_search, search)
			items = r.json()
			if "default" in items:
				for item in items['default']:
					print "%s - removing" % item['sha256']
					r = urllib2.urlopen(url_delete+"/"+item['sha256'])
