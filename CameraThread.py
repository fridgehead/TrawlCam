import urllib, urllib2, cookielib
import httplib
import re
import Image
import StringIO
import threading

class CameraThread(threading.Thread):
	def __init__(self, ip, path):
		threading.Thread.__init__(self)
		self.ip = ip
		self.path = path
		self.kill = False


	def gotFrame(self,dat, fno):
		sbuf = StringIO.StringIO(dat)
		pi = Image.open(sbuf, "r")
		pi.save("frame-%s-%s.jpg" % (self.ip, fno), "JPEG")

	def run(self):
		h=httplib.HTTPConnection(self.ip)
		try:
			h.request('GET',self.path)
			res=h.getresponse()
		except:
			print "error!"
			self.kill = True
			exit()
		if res.status != 200:
			print "login failure, exiting.."
			self.kill = True
		print res.getheaders()
		boundary = res.getheader("content-type")
		boundary = boundary[boundary.find("boundary=")+9:]
		print "boundary string : %s" % boundary

		buf = res.read(100) 
		framenum = 0
		while not self.kill:
			if buf.count(boundary) != 2:
				buf+=res.read(100)
			else:
				sp = buf.split(boundary)
				nextchunk = 0
				for ind, part in enumerate(sp):
					imgstart = part.find(chr(0xff)+chr(0xd8)+chr(0xff))
					if imgstart != -1:
						self.gotFrame(part[imgstart:], framenum)
						print "wrote file %i" % framenum
						nextchunk = ind+1
						framenum += 1
						break
				buf = "".join(sp[nextchunk:])


