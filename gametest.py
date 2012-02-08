import pygame
import math
from random import randint
import pygame.gfxdraw
from pygame.locals import *
from CameraThread import CameraThread


class testsprite(pygame.sprite.Sprite):
	def __init__(self, pos, url):
		pygame.sprite.Sprite.__init__(self)
		self.x, self.y = pos
		self.url = url
		self.camera = None #CameraThread(url[0], url[1])
		self.stop = False
		#self.camera.start()
		self.image = pygame.image.load("lol.jpg")
		self.rect = self.image.get_rect()
		self.scale = 1
		
	def stopCamera(self):
		print "cam stop.."
		self.stop = True
		self.camera.kill = True
		self.camera.join()
		self.image = pygame.image.load("lol.jpg")
	
	def startCamera(self):
		print "cam start.."
		self.stop = False
		if self.camera != None:
			self.camera.kill = False
		self.camera = CameraThread(self.url[0], self.url[1])
		self.camera.start()
	
	def setScale(self, scale):
		self.scale = scale

	def update(self):
		if self.camera != None:
			pic = self.camera.pic
			if pic is not None:
				self.image = pygame.transform.scale(pygame.image.frombuffer(pic.tostring(), pic.size, 'RGB'), (160 * self.scale, 120 * self.scale))

				self.rect = self.image.get_rect()
		self.rect.topleft = (self.x, self.y)


pygame.init()
screen = pygame.display.set_mode((1000,680))
running = 1
spriteGroup = pygame.sprite.Group()
urllist = open("knowngood","r")
y = 0
for i in range(35):
	url = urllist.readline()
	url = url[7:]
	ip = url[:url.find('/')]
	path = url[url.find('/'):] 
	x = i % 6
	if x == 5:
		y+=1
		y %= 5
	g = testsprite((160 * x,120 * y), (ip, path))
	spriteGroup.add(g)
	g.startCamera()
	


while running:
	for event in pygame.event.get():
		if event.type == KEYUP and event.key == K_ESCAPE:
			running = 0
		elif event.type == KEYUP and event.key == K_a:
			for s in spriteGroup:
				if s.stop == True:
					s.startCamera()
				else:
					s.stopCamera()
	
		else:
			pass
	current = None
	for g in spriteGroup:
		if g.rect.collidepoint(pygame.mouse.get_pos()):
			g.setScale(2)
			current = g
		else:
			g.setScale(1)

	screen.fill((0,0,0))
	spriteGroup.update()
	spriteGroup.draw(screen)
	if current != None:
		screen.blit(current.image, current.rect)
	pygame.display.flip()

#kill threads
print "telling threads to stop.."
for s in spriteGroup:
	s.stopCamera()
print "done"

pygame.quit()

