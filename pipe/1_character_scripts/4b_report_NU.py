execfile("../config.py")
from kirbybase import KirbyBase, KBError
from variousfct import *

fields = ['imgname', 'skylevel', 'prealistddev', 'seeing', 'goodstars', 'moonpercent', 'moondist', 'moonalt', 'sunalt']


db = KirbyBase()
reporttxt = ""

usedsetnames = set(map(lambda x : x[0], db.select(imgdb, ['recno'], ['*'], ['setname'])))
for setname in usedsetnames:
	
	reporttxt += "\n\n      ########### %10s    ########\n\n"%setname
	setreport = db.select(imgdb, ['gogogo','setname'], ['True', setname], fields, sortFields=['skylevel'], returnType='report')
	reporttxt += setreport

reporttxtfile = open(os.path.join(workdir, "report_skylevel.txt"), "w")
reporttxtfile.write(reporttxt)
reporttxtfile.close()


