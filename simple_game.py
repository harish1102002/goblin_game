import pygame
pygame.init()

win=pygame.display.set_mode((850,480))

walkleft = [pygame.image.load('Game/L1.png'),pygame.image.load('Game/L2.png'),pygame.image.load('Game/L3.png'),pygame.image.load('Game/L4.png'),pygame.image.load('Game/L5.png'),pygame.image.load('Game/L6.png'),pygame.image.load('Game/L7.png'),pygame.image.load('Game/L8.png'),pygame.image.load('Game/L9.png')]

walkright = [pygame.image.load('Game/R1.png'),pygame.image.load('Game/R2.png'),pygame.image.load('Game/R3.png'),pygame.image.load('Game/R4.png'),pygame.image.load('Game/R5.png'),pygame.image.load('Game/R6.png'),pygame.image.load('Game/R7.png'),pygame.image.load('Game/R8.png'),pygame.image.load('Game/R9.png')]

walklefte = [pygame.image.load('Game/L1E.png'),pygame.image.load('Game/L2E.png'),pygame.image.load('Game/L3E.png'),pygame.image.load('Game/L4E.png'),pygame.image.load('Game/L5E.png'),pygame.image.load('Game/L6E.png'),pygame.image.load('Game/L7E.png'),pygame.image.load('Game/L8E.png'),pygame.image.load('Game/L9E.png')]

walkrighte = [pygame.image.load('Game/R1E.png'),pygame.image.load('Game/R2E.png'),pygame.image.load('Game/R3E.png'),pygame.image.load('Game/R4E.png'),pygame.image.load('Game/R5E.png'),pygame.image.load('Game/R6E.png'),pygame.image.load('Game/R7E.png'),pygame.image.load('Game/R8E.png'),pygame.image.load('Game/R9E.png')]

hit=pygame.mixer.Sound('Game/hit.mp3')
bullets=pygame.mixer.Sound('Game/bullet.mp3')
music=pygame.mixer.music.load('Game/music.mp3')
pygame.mixer.music.play(-1)

bg = pygame.image.load('Game/bg.jpg')
stand = [pygame.image.load('Game/standing.png')]
defeat=pygame.image.load('Game/defeat.jpg')

class game(object):
	def __init__ (self,x,y,w,h):
		self.x=x
		self.y=y
		self.w=w
		self.h=h
		self.v=5
		self.l=False
		self.r=True
		self.wc=0
		self.run = True
		self.jump=False
		self.c=10
		self.i=1
	def disp(self,win,g):
		global s,bg,walkleft,walkright,bullet,score
		win.blit(bg,(0,0))
		win.blit(pygame.font.SysFont('comicsans',30,True).render('Score: '+ str(score),1,(0,0,0)),(630,10))
		if(self.wc+1>=27):
			self.wc=0
		if(self.l):
		  s=walkleft
		  self.wc+=1
		  win.blit(s[self.wc//3],(self.x,self.y))
		elif(self.r):
		  s=walkright
		  self.wc+=1
		  win.blit(s[self.wc//3],(self.x,self.y))
		else:
			win.blit(s[0],(self.x,self.y))
		for b in bullet:
			if(abs(g.x-b[0]+32)<15):
				bullet.pop(bullet.index(b))
				hit.play()
				score+=5
				goblin.prog-=1
			if(b[0]>=850 or b[0]<=0):
				bullet.pop(bullet.index(b))
		for b in range(len(bullet)):
			if(bullet[b][2]):
				bullet[b][0]+=self.v*1.1
			else:
				bullet[b][0]-=self.v*1.1
			pygame.draw.ellipse(win,(0,0,0),(bullet[b][0],bullet[b][1],15,5))

class enemy(object):
	def __init__ (self,x,y,w,h):
		self.x=x
		self.prog=50
		self.y=y+5
		self.w=w
		self.h=h
		self.v=4
		self.d=1
		self.s=walklefte
		self.wct=0
	def disp(self,win,p):
		if(self.wct>=26):
			self.wct=0
		if(self.x<=1):
			self.d=0
		if(self.x>=800):
			self.d=1
		if(self.d):
			self.s=walklefte
			self.x-=self.v
			self.wct+=1
		else:
			self.s=walkrighte
			self.x+=self.v
			self.wct+=1
		pygame.draw.rect(win,(0,0,0),(self.x+15,self.y-15,50,10))
		pygame.draw.rect(win,(0,255,0),(self.x+15,self.y-15,self.prog,10))
		win.blit(self.s[self.wct//3],(self.x,self.y))

s=stand
clock = pygame.time.Clock()
bullet=[]
score=0
pos=0
player=game(100,416,64,64)
goblin=enemy(500,416,64,64)
while player.run:
	clock.tick(27)
	if(goblin.x<player.x+7 and goblin.x>player.x-7 and player.y>330):
		pygame.draw.rect(win,(0,0,0),(0,0,850,480))
		pygame.mixer.music.stop()
		win.blit(defeat,(50,30))
		pygame.display.update()
		for i in range(5):
			for e in pygame.event.get():
				if e.type==pygame.QUIT:
					exit()
			pygame.time.delay(600)
		break
	for e in pygame.event.get():
		if e.type==pygame.QUIT:
			player.run=False
	k=pygame.key.get_pressed()
	if k[pygame.K_LEFT]:
		player.l=True
		player.r=False
		player.x=max(player.x-player.v,0)
	elif k[pygame.K_RIGHT]:
		player.l=False
		player.r=True
		player.x=min(player.x+player.v,850-player.w)
	else:
		player.l=False
		player.r=False
	if k[pygame.K_DOWN]:
		if len(bullet)<5:
			if(s==walkleft):
				s1=0
				j=4*len(bullet)-10
			else:
				s1=1
				j=65-4*len(bullet)
			bullet.append([player.x+j,player.y+20,s1])
			bullets.play()
	if not player.jump:
		if k[pygame.K_SPACE]:
			player.jump=True
	else:
		if(-10<=player.c):
			player.i=1
			if(player.c<0):
				player.i=-1
			player.y=max(player.y-(player.c**2)*0.5*player.i,0)
			player.c-=1
		else:
			player.jump=False
			player.c=10
	if(goblin.prog<=0):
		goblin=enemy(pos*800,416,64,64)
		pos=(pos+1)%2
	player.disp(win,goblin)
	goblin.disp(win,player.x)
	pygame.display.update()
pygame.quit()