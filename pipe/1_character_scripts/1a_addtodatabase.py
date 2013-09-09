# 
#	This is the first script.
#	We add images to the database, read their headers, etc.
#	If no database exists, we create one. If not we add the images, after some test.
#


execfile("../config.py")
import glob
import pyfits
import datetime
from kirbybase import KirbyBase, KBError
from variousfct import *
from headerstuff import *

#	We define some mandatory fields in the database :

minimaldbfields = ['imgname:str', 'treatme:bool', 'gogogo:bool', 'whynot:str', 'testlist:bool', 'testcomment:str',
'telescopename:str', 'setname:str', 'rawimg:str',
'scalingfactor:float', 'pixsize:float','date:str','datet:str','jd:str','mjd:float',
'telescopelongitude:str', 'telescopelatitude:str', 'telescopeelevation:float',
'exptime:float','gain:float', 'readnoise:float', 'rotator:float', 'saturlevel:float',
'preredcomment1:str', 'preredcomment2:str', 'preredfloat1:float', 'preredfloat2:float']



# Function that selects the one that reads the header, according to telescopename

def readheader(telescopename, rawimg):
	if telescopename == "EulerC2":
		dbdict = eulerc2header(rawimg)
	elif telescopename == "EulerCAM":
		dbdict = eulercamheader(rawimg)
	elif telescopename == "Mercator":
		dbdict = mercatorheader(rawimg)
	elif telescopename == "Liverpool":
		dbdict = liverpoolheader(rawimg)
	elif telescopename == "MaidanakSITE":
		dbdict = maidanaksiteheader(rawimg)
	elif telescopename == "MaidanakSI":
		dbdict = maidanaksiheader(rawimg)
	elif telescopename == "Maidanak2k2k":
		dbdict = maidanak2k2kheader(rawimg)
	elif telescopename == "HCT":
		dbdict = hctheader(rawimg)
	elif telescopename == "HoLi":
		dbdict = holiheader(rawimg)
	elif telescopename == "SMARTSandicam":
		dbdict = smartsandicamheader(rawimg)
	elif telescopename == 'skysim':
		dbdict = skysimheader(rawimg)
	elif telescopename == "NOHEADER":
		dbdict = noheader(rawimg)	
	else:
		raise mterror("Unknown telescope.")	

	return dbdict
	


print "Here we go !"
print "You want to add the set " + setname + " to the database."
print rawdir
if not os.path.isdir(rawdir):
	raise mterror("This directory does not exist!")
fitsfiles = glob.glob(os.path.join(rawdir, "*.fits"))
print "Number of images :", len(fitsfiles)
#fitslist = sorted(map((lambda x: x.split("/")[-1]), fitsfiles))
fitslist = sorted([os.path.basename(filepath) for filepath in fitsfiles])

proquest(askquestions)

print "You did not forget to flip these images (if needed), right ?"
proquest(askquestions)

db = KirbyBase()

if os.path.isfile(imgdb):

	print "Database exists ! I will ADD these new images."
	proquest(askquestions)
	backupfile(imgdb, dbbudir, "adding"+setname)
	
	# We check if all the fields are there
	presentfields = db.getFieldNames(imgdb)
	mandatoryfields = [field.split(':')[0] for field in minimaldbfields]
	mandatoryfields.append('recno')
	if not set(mandatoryfields).issubset(set(presentfields)) :
		raise mterror("Your database misses mandatory fields ! Change this and come back. ")
	
	# We check if the setname is already used
	usedsetnames = map(lambda x : x[0], db.select(imgdb, ['recno'], ['*'], ['setname']))
	usedsetnameshisto = "".join(["%10s : %4i\n"%(item, usedsetnames.count(item)) for item in set(usedsetnames)])
	#usedsetnameshisto = usedsetnames
	print "In the database, we already have :"
	print usedsetnameshisto
	proquest(askquestions)
	if setname in usedsetnames:
		raise mterror("Your new setname is already used !")
	
	# We get a list of the rawimg we have already in the db :
	knownrawimgs = map(lambda x : x[0], db.select(imgdb, ['recno'], ['*'], ['rawimg']))
	
	# Ok, if we are here then we can insert our new images into the database.
	for i, fitsfile in enumerate(fitslist):
		print i+1, fitsfile
		rawimg = os.path.join(rawdir, fitsfile)
		
		dbdict = readheader(telescopename, rawimg)
		
		# We check if this image already exists in the db. If yes, we just skip it.
		# For this we compare the "rawimg", that is the path of the image file. You might want to adapt this to use e.g. the imgname ?
		# But keep in mind that the imgname contains the setname !
				
		if dbdict["rawimg"] in knownrawimgs:
			print "I already have this one ! (-> I skip it without updating anything)"
			continue

		# We have to insert image by image into our database.
		db.insert(imgdb, dbdict)
	
	#sys.exit()
	#os.remove(imgdb)

else :
	print "A NEW database will be created."
	proquest(askquestions)
	db.create(imgdb, minimaldbfields)

	table = []
	for i, fitsfile in enumerate(fitslist):
		print i+1, "/", len(fitslist), " : ", fitsfile
		rawimg = os.path.join(rawdir, fitsfile)	
		
		dbdict = readheader(telescopename, rawimg)
		
		table.append(dbdict) # In this case we build a big list for batch insertion.

	# Here we do a "batch-insert" of a list of dictionnaries
	db.insertBatch(imgdb,table)

db.pack(imgdb) # to erase the blank lines

print "Ok, Done."
print "If you work with several telescopes or sets you might want to change the treatme-flags at this point."
print "Or, more likely : update the settings and run this script again, to add further images from another directory/telescope."



