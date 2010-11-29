#
#	write the input file in.txt and deconv.txt for the deconvolution
#

execfile("../config.py")
from kirbybase import KirbyBase, KBError
#from variousfct import *
from readandreplace_fct import *
import star
import shutil
from variousfct import *


	# count nbr of images
	
db = KirbyBase()
images = db.select(imgdb, [deckeyfilenum], ['\d\d*'], returnType='dict', useRegExp=True, sortFields=[deckeyfilenum]) # WARNING the sorting is important !!!!!!!
nbimg = len(images)
#nbimg = int(os.popen("ls -1 " + decdir + "g???.fits" + " | wc -l").readlines()[0])
print "Number of images :", nbimg


	# read params of point sources
ptsrc = star.readmancat(ptsrccat)
nbptsrc = len(ptsrc)
print "Number of point sources :", nbptsrc

proquest(askquestions)

	# deconv.txt
	
deconv_template = justread(deconv_template_filename)
deconvdict = {"$nbimg$": str(nbimg), "$nbptsrc$":str(nbptsrc)}
deconvtxt = justreplace(deconv_template, deconvdict)
deconvfile = open(os.path.join(decdir, "deconv.txt"), "w")
deconvfile.write(deconvtxt)
deconvfile.close()
print "Wrote deconv.txt"
	# in.txt

		# int and pos of the sources
intandposblock = ""
print "Reformatted point sources :"
for i in range(nbptsrc):
	if ptsrc[i].flux < 0.0 :
		raise mterror("Please specify a positive flux for your point sources !")
	intandposblock = intandposblock + nbimg * (str(ptsrc[i].flux) + " ") + "\n"
	intandposblock = intandposblock + str(2*ptsrc[i].x-0.5) + " " + str(2*ptsrc[i].y-0.5) + "\n"
	print str(ptsrc[i].flux), str(2*ptsrc[i].x-0.5), str(2*ptsrc[i].y-0.5)
intandposblock	= intandposblock.rstrip("\n") # remove the last newline
	
		# other params
otheriniblock = nbimg * "1.0 0.0 0.0 0.0\n"
otheriniblock = otheriniblock.rstrip("\n") # remove the last newline

in_template = justread(in_template_filename)
indict = {"$otheriniblock$": otheriniblock, "$intandposblock$": intandposblock}
intxt = justreplace(in_template, indict)
infile = open(os.path.join(decdir, "in.txt"), "w")
infile.write(intxt)
infile.close()
print "Wrote in.txt"

	# Is a worse input file possible ?
	# Yes !!!!
	# Here comes "fwhm-des-G.txt" :

# Important for this point : "images" is sorted by deckeyfilenum

# just a quick check of what we have :
#for image in images:
#	print "%s : %9.4f pixels = %9.4f arcsec (%s)" % (image[deckeyfilenum], image["seeingpixels"], image["seeing"], image["imgname"])

fwhmtxt = "\n".join(["%.4f" % image["seeingpixels"] for image in images]) + "\n"
fwhmfile = open(os.path.join(decdir, "fwhm-des-G.txt"), "w")
fwhmfile.write(fwhmtxt)
fwhmfile.close()
print "Wrote fwhm-des-G.txt"



print "I've prepared the input files for %s." % deckey
	
	
