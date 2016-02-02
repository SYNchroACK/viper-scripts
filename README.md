Viper Scripts
===================


This is a collection of scripts to interact with the Viper malware database.  

----------


viperupload.py
-------------
viperupload.py provides a method of doing bulk insert and tagging, useful for interaction with other scripts.

Usage:
Generic syntax is in the following pattern
```
python viperupload.py -s sample.exe -t tags
```

Examples:
Bulk Upload
To upload a folder of malware (named samples) and tag them all as "APT" and "Energy"
```
python viperupload.py -d samples/ -t APT Energy
```
Single Upload
```
python viperupload.py -s sample.exe -t Crimeware BlackPOS
```

Note:
----
viperupload.py will also automatically calculate and add imphash as a tag.
