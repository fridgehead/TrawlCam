from CameraThread import CameraThread

threads = []
urllist = open("knowngood", "r")

for url in urllist:
	url = url[7:]
	ip = url[:url.find('/')]
	path = url[url.find('/'):] 
	print ip, path 

	c = CameraThread(ip.strip(), path.strip())
	threads.append(c)
	c.start()

while len(threads) > 0:
	try:
		threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
	except KeyboardInterrupt:
	        print "Ctrl-c received! Sending kill to %i threads... " % len(threads)
		for t in threads:
			t.kill = True
		print "..done"
print "done!"
