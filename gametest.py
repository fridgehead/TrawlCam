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
		self.camera = CameraThread(url[0], url[1])
		self.stop = True
		self.camera.start()
		self.image = pygame.image.load("lol.jpg")
		self.rect = self.image.get_rect()
		
	def stopCamera(self):
		self.stop = True
		self.camera.kill = True

	def update(self):
		pic = self.camera.pic
		if pic is not None:
			self.image = pygame.transform.scale(pygame.image.frombuffer(pic.tostring(), pic.size, 'RGB'), (160,120))

			self.rect = self.image.get_rect()


pygame.init()
screen = pygame.display.set_mode((800,480))
running = 1
spriteGroup = pygame.sprite.Group()
spriteGroup.add(testsprite((0,0), ("127.0.0.1:9000", "/")))



while running:
	for event in pygame.event.get():
		if event.type == KEYUP and event.key == K_ESCAPE:
			running = 0
		else:
			pass

	screen.fill((120,0,0))
	spriteGroup.update()
	spriteGroup.draw(screen)
	pygame.gfxdraw.line(screen, 100,100,200,200, (255,255,255))
	pygame.display.flip()

#kill threads
print "telling threads to stop.."
for s in spriteGroup:
	s.stopCamera()
print "done"

pygame.quit()

