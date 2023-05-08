import os
import subprocess
import sys

# for local testing
# os.chdir("/storage/emulated/0/Download/mgit/test/")

#pathtoplugins = myplugins/
#indexfile = README.md
#assetfiles = https://github.com/zuckung/test/releases/download/Latest/
#pluginurl = https://github.com/zuckung/test/tree/main/myplugins/
#headerfile = res/header.txt
#picturefile = res/icon.png


# read paths and files
with open("res/paths.txt") as f:
	for line in f:
		line = str((line.strip()))
		if line.find("pathtoplugins") == 0:
			pathtoplugins = line.split(" = ")[1]
		elif line.find("indexfile") == 0:
			indexfile = line.split(" = ")[1]
		elif line.find("assetfiles") == 0:
 			assetfiles = line.split(" = ")[1]
		elif line.find("pluginurl") == 0:
			pluginurl = line.split(" = ")[1]
		elif line.find("header") == 0:
			headerfile = line.split(" = ")[1]
		elif line.find("picturefile") == 0:
			picturefile = line.split(" = ")[1]

# checks for arguments in .py call
if len(sys.argv) < 2:
	print("no arguments on call, zipping all plugins")
	entries = os.listdir(pathtoplugins)
	entries = sorted(entries)
	# for each plugin directory
	for entry in entries:

		os.chdir(pathtoplugins) # todo check how deep
        
		# checks for spaces in folder and renames it
		if str(entry.find(" ")) != "-1":
			spaced  = entry + "/"
			entry = spaced.replace(" ", ".")
			subprocess.run(["mv", spaced , entry], stdout=subprocess.DEVNULL)	
			print("found a folder with spaces in name and renamed it: " + entry)
		# zipping
		subprocess.run(["zip", "-r", "../" + entry + ".zip", entry], stdout=subprocess.DEVNULL) 
		os.chdir('../')
		print(entry + " zipping DONE")
		subprocess.run(["mv", entry + ".zip", "zip/" + entry + ".zip"], stdout=subprocess.DEVNULL)
		
# has arguments       
else:    
	#formating arguments
	changed = str(sys.argv)
	pos = changed.index(".py', '") + 7
	changed = changed[pos:]
	changed = changed.replace("', '"," ")
	changed = changed.replace("']","")
	print("arguments are : " + changed)


	plugins = set()
	for f in changed.split("%25%25%25"):
		if not "myplugins" in f:
			continue
		path = f.split(os.sep)
		index = path.index("myplugins") + 1
		if index >= len(path):
			continue
		plugins.add(path[index])
		if plugins:
			print("The following plugins have changed:")
			for p in plugins:
				print(p)
				os.chdir('myplugins/')
				x = p.replace(" ", ".")
				subprocess.run(["zip", "-r", "../" + x + ".zip", p], stdout=subprocess.DEVNULL)
				os.chdir('../')
		else:
			print("No plugin changes have been detected.")