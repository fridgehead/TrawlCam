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
		self.camera = CameraThread(url[0], url[1])
		self.stop = False
		self.camera.start()
		self.image = pygame.image.load("lol.jpg")
		self.rect = self.image.get_rect()
		
	def stopCamera(self):
		print "cam stop.."
		self.stop = True
		self.camera.kill = True
		self.camera.join()
	
	def startCamera(self):
		print "cam start.."
		self.stop = False
		self.camera.kill = False
		self.camera = CameraThread(self.url[0], self.url[1])
		self.camera.start()

	def update(self):
		pic = self.camera.pic
		if pic is not None:
			self.image = pygame.transform.scale(pygame.image.frombuffer(pic.tostring(), pic.size, 'RGB'), (160,120))

			self.rect = self.image.get_rect()
		self.rect.topleft = (self.x, self.y)


pygame.init()
screen = pygame.display.set_mode((1000,680))
running = 1
spriteGroup = pygame.sprite.Group()
spriteGroup.add(testsprite((0,0), ("127.0.0.1:9000", "/")))



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

	screen.fill((0,0,0))
	spriteGroup.update()
	spriteGroup.draw(screen)
	pygame.display.flip()

#kill threads
print "telling threads to stop.."
for s in spriteGroup:
	s.stopCamera()
print "done"

pygame.quit()

