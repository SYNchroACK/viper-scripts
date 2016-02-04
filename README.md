Viper Scripts
===================


This is a collection of scripts to interact with the Viper malware database.  

----------

vipermanage.py
-------------
vipermanage.py is a wrapper around the Viper DB that allows for easy upload, download, searching, and removing samples. 

```
usage: vipermanage.py [-h] (-u | -d | -l | -r) [-s SAMPLE] [-S SEARCH]
                      [-t TAGS [TAGS ...]] [-D DIR]

Tool to manage samples in the Viper Malware DB

optional arguments:
  -h, --help            show this help message and exit
  -u, --upload          Upload Sample(s)
  -d, --download        Download Sample(s)
  -l, --list            List Sample(s)
  -r, --remove          Remove Sample(s)
  -s SAMPLE, --sample SAMPLE
                        Single Sample
  -S SEARCH, --search SEARCH
                        Search for sample (SHA256)
  -t TAGS [TAGS ...], --tags TAGS [TAGS ...]
                        Tags to search on or add
  -D DIR, --dir DIR     Directory to upload or Dest Directory for Download

```
Note: The functionality of viperupload.py has been combined with vipermanage, please use this library from now on.

Examples:
Bulk Upload
To upload a folder of malware (named samples) and tag them all as "APT" and "Energy"
```
vipermanage.py --upload --dir samples/ -t APT Energy
```
Single Upload
```
vipermanage.py --upload --sample sample.exe -t lightserver APT
```
Remove a bulk collection (according to tag)
```
python vipermanage.py --remove -t BlackPOS
```
Remove a Sample
```
vipermanage.py --remove --sample  29d8dc863427c8e37b75eb738069c2172e79607acc7b65de6f8086ba36abf051
```
Download a sample
```
vipermanage.py --download --search 29d8dc863427c8e37b75eb738069c2172e79607acc7b65de6f8086ba36abf051
```
Download all of a certain tag
```
vipermanage.py --download -t BlackPOS
```
List all of a tag
```
vipermanage.py --list -t BlackPOS
```
List / Search for a single sample
```
vipermanage.py --list --search 29d8dc863427c8e37b75eb738069c2172e79607acc7b65de6f8086ba36abf051
```

Note:
----
vipermanage.py will also automatically calculate and add imphash as a tag.

