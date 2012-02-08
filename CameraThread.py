import urllib, urllib2, cookielib
import httplib
import re
import Image
import StringIO
import threading
import sys

class CameraThread(threading.Thread):
	def __init__(self, ip, path):
		threading.Thread.__init__(self)
		self.ip = ip.strip()
		self.path = path.strip()
		self.kill = False
		self.pic = None
		print "created camera for ip: %s, url: %s;" %(ip, path)


	def gotFrame(self,dat, fno):
		sbuf = StringIO.StringIO(dat)

		self.pic = Image.open(sbuf, "r")
#		pi.save("frame-%s-%s.jpg" % (self.ip, fno), "JPEG")

	def run(self):
		h=httplib.HTTPConnection(self.ip)
		try:
			h.request('GET',self.path)
			res=h.getresponse()
			if res.status != 200:
				print "login failure, exiting.."
				self.kill = True
			boundary = res.getheader("content-type")
			boundary = boundary[boundary.find("boundary=")+9:]

			buf = res.read(100) 
			framenum = 0
			while self.kill == False:
				if buf.count(boundary) != 2:
					buf+=res.read(100)
				else:
					sp = buf.split(boundary)
					nextchunk = 0
					for ind, part in enumerate(sp):
						imgstart = part.find(chr(0xff)+chr(0xd8)+chr(0xff))
						if imgstart != -1:
							self.gotFrame(part[imgstart:], framenum)
							#print "wrote file %i" % framenum
							nextchunk = ind+1
							framenum += 1
							break
					buf = "".join(sp[nextchunk:])

		except:
			print "error for : " + self.ip , sys.exc_info()
			h.close()
			self.kill = True
		print "thread deaded!"	
