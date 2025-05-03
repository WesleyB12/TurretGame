# based on a game i made in scratch
#pygame
import pygame,math
pygame.init()
x=960
y=900
screen = pygame.display.set_mode((1920,1080))       
pygame.display.set_caption('0')
my_font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
running=True
turrets=[]
TRACK=[(0,50),(100,1040),(200,40),(300,1040),(400,40),(500,1040),(600,500),(1920,500)]
dists=[]
currentturretbeingbought='NONE'
speed=60
info={'normal':{'color':(255,59,59),'border':(96,133,135),'health':2,'speed':4,'price':2,'size':60,'healthbarsize':60},
      'fast':{'color':(255,233,18),'border':(96,133,135),'health':1,'speed':8,'price':2,'size':60,'healthbarsize':60},
      'strong':{'color':(12,179,29),'border':(96,133,135),'health':8,'speed':2,'price':3,'size':100,'healthbarsize':80},
      'multiple':{'color':(124,148,170),'border':(50,75,230),'health':140,'speed':1.5,'price':3,'size':90,'healthbarsize':120},
      'verystrong':{'color':(8,112,18),'border':(40,40,40),'health':45,'speed':1,'price':3,'size':110,'healthbarsize':200},
      'veryfast':{'color':(0,26,255),'border':(0,0,0),'health':2,'speed':16,'price':2,'size':40,'healthbarsize':50},
      'ultrafast':{'color':(20,60,255),'border':(0,0,0),'health':2,'speed':25,'price':2,'size':30,'healthbarsize':45},
      'instantfast':{'color':(255,255,255),'border':(0,0,0),'health':50,'speed':35,'price':2,'size':25,'healthbarsize':40},
      'tank':{'color':(30,80,30),'border':(30,30,50),'health':1000,'speed':0.3,'price':10,'size':120,'healthbarsize':400},
      'spreader':{'color':(200,200,255),'border':(0,0,0),'health':10000,'speed':0.24,'price':100,'size':150,'healthbarsize':800},
      'teleporter':{'color':(0,0,0),'border':(255,255,255),'health':20,'speed':45,'price':2,'size':20,'healthbarsize':35}}
      
splitinfo={'multiple':{'number':20,'type':'fast'},'verystrong':{'number':1,'type':'strong'},'veryfast':{'number':3,'type':'fast'},
           'ultrafast':{'number':5,'type':'veryfast'},'instantfast':{'number':5,'type':'ultrafast'},'tank':{'number':1,'type':'verystrong'},
           'spreader':{'number':80,'type':'multiple'},'teleporter':{'number':10,'type':'instantfast'}}
levels=[['normal',10,5,1],['normal','fast',20,5,2],['normal','fast','normal',33,4,3],['normal',40,5,1],['fast',45,1,1],['normal','fast','strong',30,2,3],['ultrafast',2,100,1],
        ['verystrong','fast','normal',20,30,3],['fast','normal',200,10,2],['ultrafast','fast','normal','strong','fast','normal','fast','normal',30,30,8],['normal',300,8,1],
        ['tank','normal','normal','normal','normal',5,100,5],['fast','veryfast','normal','strong',300,20,4],['fast',300,1,1],['instantfast',1,1,1],['multiple','veryfast',100,20,2],
        ['multiple','verystrong','strong',50,10,3],['verystrong','multiple',45,1,2],['tank',8,100,1],['instantfast',4,100,1],
        ['veryfast','fast','verystrong','multiple','normal',300,10,5],['tank',12,50,1],['spreader',1,1,1],['multiple','tank',100,10,2]]
turreticon=pygame.transform.scale(pygame.image.load('turretim.png'),(80,50))
doubleturreticon=pygame.transform.scale(pygame.image.load('doubleturret.png'),(80,50))
fastturreticon=pygame.transform.scale(pygame.image.load('fastturret.png'),(80,50))
boom=pygame.transform.scale(pygame.image.load('boom.png'),(140,100))
turretim=pygame.transform.scale(pygame.image.load('turretim.png'),(110,70))
doubleturretim=pygame.transform.scale(pygame.image.load('doubleturret.png'),(110,70))
fastturretim=pygame.transform.scale(pygame.image.load('fastturret.png'),(140,70))
rocketturretim=pygame.transform.scale(pygame.image.load('rocketturret.png'),(110,70))
rocketturreticon=pygame.transform.scale(pygame.image.load('rocketturret.png'),(80,50))
rocketim=pygame.transform.scale(pygame.image.load('rocket.png'),(80,50))
tripleturreticon=pygame.transform.scale(pygame.image.load('tripleturret.png'),(80,50))
quadlaunchericon=pygame.transform.scale(pygame.image.load('quadlauncher.png'),(80,50))
turretinfo={'single':{'image':turretim,'firingimage':pygame.transform.scale(pygame.image.load('shootingturret.png'),(110,70)),'firerate':100,'range':500,'dmg':1},
            'double':{'image':doubleturretim,'firingimage':pygame.transform.scale(pygame.image.load('shootingdoubleturret.png'),(110,70)),'firerate':45,'range':400,'dmg':1.1},
            'fast':{'image':fastturretim,'firingimage':pygame.transform.scale(pygame.image.load('shootingfastturret.png'),(140,70)),'firerate':10,'range':300,'dmg':0.4},
            'rocket':{'image':rocketturretim,'firingimage':pygame.transform.scale(pygame.image.load('firingrocketturret.png'),(140,70)),'firerate':60,'range':9999,'dmg':0.4},
            'triple':{'image':pygame.transform.scale(pygame.image.load('tripleturret.png'),(110,70)),'firingimage':pygame.transform.scale(pygame.image.load('shootingtripleturret.png'),(110,70)),'firerate':5,'range':450,'dmg':2.2},
            'quadlauncher':{'image':pygame.transform.scale(pygame.image.load('quadlauncher.png'),(110,70)),'firingimage':pygame.transform.scale(pygame.image.load('firingquadlauncher.png'),(110,70)),'firerate':12,'range':9999,'dmg':1.2}}
explosions=[]
mouseaction=-1
money=150000
lives=30
spawning=[]
currentspawn=None
currentpause=0
currentspawnnum=0
lefttospawn=0
button=pygame.image.load('Playbutton.png')
leveldone=False
level=0
pause=False
validturret=False
(mousex,mousey)=pygame.mouse.get_pos()
rockets=[]
selectedturret=None

def get_validturret(x,y):
    pygame.draw.lines(screen,(148,87,68),False,TRACK,100)
    if screen.get_at((x,y))==(148,87,68,255):
        return False
    for turret in turrets:
        if math.dist(turret.pos,(x,y))<70:
            return False
    return True
for seg in TRACK: 
    try:
        dists.append(math.dist(seg,TRACK[TRACK.index(seg)+1]))
    except IndexError:
        pass    
def drawhealthbars():
    for enemy in enemies:
        if enemy.health!=enemy.maxhealth:
            pygame.draw.line(screen,(0,0,0),(enemy.pos[0]-(enemy.healthbarsize/2),enemy.pos[1]-40),(enemy.pos[0]+(enemy.healthbarsize/2),enemy.pos[1]-40),20)
            pygame.draw.line(screen,((math.sin((enemy.health*(math.pi/2)/enemy.maxhealth)+(math.pi/2)))*255,109,29),(enemy.pos[0]-(enemy.healthbarsize/2),enemy.pos[1]-40),(enemy.pos[0]+((enemy.health/enemy.maxhealth)*enemy.healthbarsize)-(enemy.healthbarsize/2),enemy.pos[1]-40),20)
def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
    return rotated_image, new_rect
def spawn(enemytypes,quantity,pause):
    global spawning
    global currentspawn
    global currentspawnnum
    global currentpause
    global lefttospawn
    spawning=[enemytypes,'END',quantity,pause]
    currentspawn=spawning[0][0]
    currentspawnnum=0
    currentpause=0
    lefttospawn=quantity
class Turret:
    def __init__(self,x,y,type): 
        self.type=type
        self.pivot=(34, 65)
        self.image=turretinfo[self.type]['image']
        turrets.append(self)
        self.rotation=0
        self.pos=(x,y)
        self.range=turretinfo[self.type]['range']
        self.cooldown=30
        self.damage=turretinfo[self.type]['dmg']
        self.timetofire=turretinfo[self.type]['firerate']
        self.firing=False
        self.shootingim=turretinfo[self.type]['firingimage']
    def update(self):
        global money
        self.enemyprog=0
        self.enemyob=None
        for enemy in enemies:
            if enemy.totalprog>self.enemyprog and math.dist(self.pos,enemy.pos)<self.range:
                self.enemyob=enemy
                self.enemyprog=enemy.totalprog    
        if self.enemyob!=None:    
            if self.pos[1]>self.enemyob.pos[1]:    
                self.rotation=math.atan((self.pos[0]-self.enemyob.pos[0])/(self.pos[1]-self.enemyob.pos[1]))*180/math.pi+90
            else:
                self.rotation=math.atan((self.pos[0]-self.enemyob.pos[0])/(self.pos[1]-self.enemyob.pos[1]))*180/math.pi+270
        if self.cooldown<1 and self.enemyob!=None:
           self.image=self.shootingim
           self.cooldown=self.timetofire
           self.firing=True
           self.enemyob.health-=self.damage
           if self.enemyob.health<=0:
                try:
                    for i in range(splitinfo[self.enemyob.type]['number']):
                        Enemy(splitinfo[self.enemyob.type]['type'],self.enemyob.pos[0],self.enemyob.pos[1],self.enemyob.angle,self.enemyob.progress,self.enemyob.currentseg
                              ,self.enemyob.totalprog,self.enemyob.currentdist)     
                        self.enemyob.pos=(self.enemyob.pos[0]+(self.enemyob.speed*5*math.cos(self.enemyob.angle)),
                                          self.enemyob.pos[1]+(self.enemyob.speed*5*math.sin(self.enemyob.angle)))
                        self.enemyob.progress+=self.enemyob.speed*5
                        self.enemyob.totalprog+=self.enemyob.speed*5
                except KeyError:
                   pass
                enemies.remove(self.enemyob)
                money+=self.enemyob.price
        if self.cooldown==self.timetofire-4:
            self.image=turretinfo[self.type]['image']
            self.firing=False
        self.cooldown-=1
        screen.blit(rot_center(self.image,self.rotation,self.pos[0],self.pos[1])[0],rot_center(self.image,self.rotation,self.pos[0],self.pos[1])[1])
        if self.firing:
            pygame.draw.circle(screen,(30,30,30),(self.pos[0]+(math.cos(self.rotation*180/math.pi)*-90),self.pos[1]+(math.sin(self.rotation*math.pi/180)*-90)),5)
class RocketLauncher(Turret):
    def __init__(self,x,y,type):

        super().__init__(x,y,type)
    def update(self):
        global money
        self.enemyprog=0
        self.enemyob=None
        for enemy in enemies:
            if enemy.totalprog>self.enemyprog and math.dist(self.pos,enemy.pos)<self.range:
                self.enemyob=enemy
                self.enemyprog=enemy.totalprog    
        if self.enemyob!=None:    
            if self.pos[1]>self.enemyob.pos[1]:    
                try:
                    self.rotation=math.atan((self.pos[0]-self.enemyob.pos[0])/(self.pos[1]-self.enemyob.pos[1]))*180/math.pi+90
                except:
                    pass
            else:
                try:
                    self.rotation=math.atan((self.pos[0]-self.enemyob.pos[0])/(self.pos[1]-self.enemyob.pos[1]))*180/math.pi+270
                except:
                    pass
        if self.cooldown<1 and self.enemyob!=None:
            self.image=self.shootingim
            self.cooldown=self.timetofire
            self.firing=True
            Rocket(self.enemyob,self.pos[0],self.pos[1],self.damage)
        if self.cooldown==self.timetofire-4:
            self.image=turretinfo[self.type]['image']
            self.firing=False
        self.cooldown-=1
        screen.blit(rot_center(self.image,self.rotation,self.pos[0],self.pos[1])[0],rot_center(self.image,self.rotation,self.pos[0],self.pos[1])[1])
        if self.firing:
            pygame.draw.circle(screen,(30,30,30),(self.pos[0]+(math.cos(self.rotation*180/math.pi)*-90),self.pos[1]+(math.sin(self.rotation*math.pi/180)*-90)),5)
class Rocket:
    def __init__(self,enemy,x,y,dmg):
        self.pos=(x,y)
        self.enemy=enemy
        self.speed=20
        self.damage=dmg
        rockets.append(self)
        self.im=rocketim
        self.angle=0
    def update(self):
        global money
        try:
            if self.pos[0]<self.enemy.pos[0]:
                self.angle=math.atan((self.pos[1]-self.enemy.pos[1])/(self.pos[0]-self.enemy.pos[0]))
            else:
                self.angle=math.atan((self.pos[1]-self.enemy.pos[1])/(self.pos[0]-self.enemy.pos[0]))+math.pi
        except:
            pass
        self.pos=(self.pos[0]+(self.speed*math.cos(self.angle)),self.pos[1]+(self.speed*math.sin(self.angle)))   
        if math.dist(self.pos,self.enemy.pos)<20:
            for enemy in enemies:
                if math.dist(self.pos,enemy.pos)<180:
                    enemy.health-=self.damage
                if enemy.health<=0:
                    try:
                        for i in range(splitinfo[enemy.type]['number']):
                            Enemy(splitinfo[enemy.type]['type'],enemy.pos[0],enemy.pos[1],enemy.angle,enemy.progress,enemy.currentseg
                                ,enemy.totalprog,enemy.currentdist)     
                            enemy.pos=(enemy.pos[0]+(enemy.speed*5*math.cos(enemy.angle)),
                                            enemy.pos[1]+(enemy.speed*5*math.sin(enemy.angle)))
                            enemy.progress+=enemy.speed*5
                            enemy.totalprog+=enemy.speed*5
                    except KeyError:
                        pass
                    try:
                        enemies.remove(enemy)
                    except ValueError:
                        pass
                    money+=enemy.price
            rockets.remove(self)
            explosions.append([self.pos,5])
        if self.enemy not in enemies:
            self.highestprog=0
            for enemy in enemies:
                if enemy.totalprog>self.highestprog:
                    self.enemy=enemy
                    self.highestprog=self.enemy.totalprog
        screen.blit(rot_center(self.im,-self.angle*180/math.pi,self.pos[0],self.pos[1])[0],rot_center(self.im,-self.angle*180/math.pi,self.pos[0],self.pos[1])[1])
class Enemy:
    def __init__(self,type,x=TRACK[0][0],y=TRACK[0][1],angle=math.atan((TRACK[0][0]-TRACK[1][0])/(TRACK[0][1]-TRACK[1][1])),progress=0,currentseg=(TRACK[0],TRACK[1],0),
                 overallprogeress=0,currentdist=dists[0]):
        try:
            global lives
            self.type=type
            self.color=info[self.type]['color']
            self.border=info[self.type]['border']
            enemies.append(self)
            self.pos=(x,y)
            self.speed=info[self.type]['speed']
            self.progress=progress
            self.totalprog=overallprogeress
            self.angle=angle
            self.currentseg=currentseg
            self.currentdist=currentdist
            self.health=info[self.type]['health']
            self.maxhealth=self.health
            self.price=info[self.type]['price']
            self.size=info[self.type]['size']
            self.healthbarsize=info[self.type]['healthbarsize']
            if self.progress>self.currentdist:
                self.currentseg=(None,None,self.currentseg[2]+1)
                self.currentseg=(TRACK[self.currentseg[2]],TRACK[self.currentseg[2]+1],self.currentseg[2])
                self.currentdist=dists[self.currentseg[2]]
                self.progress=0
                self.pos=self.currentseg[0]
            if self.currentseg[0]==TRACK[-2] and self.progress>dists[-1]-30:
                lives-=1
                enemies.remove(self)
        except:
            enemies.remove(self)
    def update(self):
        global lives
        if self.currentseg[0][0]<self.currentseg[1][0]:
            self.angle=math.atan((self.currentseg[0][1]-self.currentseg[1][1])/(self.currentseg[0][0]-self.currentseg[1][0]))
        else:
            self.angle=math.atan((self.currentseg[0][1]-self.currentseg[1][1])/(self.currentseg[0][0]-self.currentseg[1][0]))+math.pi
        if self.currentseg[0]==TRACK[-2] and self.progress>dists[-1]-30:
            lives-=1
            enemies.remove(self)
        self.pos=(self.pos[0]+(self.speed*math.cos(self.angle)),self.pos[1]+(self.speed*math.sin(self.angle)))    
        if self.progress>self.currentdist:
            try:
                self.currentseg=(None,None,self.currentseg[2]+1)
                self.currentseg=(TRACK[self.currentseg[2]],TRACK[self.currentseg[2]+1],self.currentseg[2])
                self.currentdist=dists[self.currentseg[2]]
                self.progress=0
                self.pos=self.currentseg[0]
            except IndexError:
                enemies.remove(self)
        self.progress+=self.speed
        self.totalprog+=self.speed
        pygame.draw.rect(screen,self.color,pygame.Rect(self.pos[0]-(self.size/2),self.pos[1]-(self.size/2),self.size,self.size))
        pygame.draw.rect(screen,self.border,pygame.Rect(self.pos[0]-(self.size/2),self.pos[1]-(self.size/2),self.size,self.size),5,1)
enemies=[]
Enemy('normal')
spawn(levels[0][:levels[0][-1]],quantity=levels[0][-3],pause=levels[0][-2])
while running:
    validturret=get_validturret(mousex,mousey)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    screen.fill((85, 219, 64))
    pygame.draw.lines(screen,(148,87,68),False,TRACK,60)
    (mousex,mousey)=pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        turretgotselected=False
        for turret in turrets:
            if math.dist((mousex,mousey),turret.pos)<35:
                selectedturret=turret
                turretgotselected=True
        if not turretgotselected:
            selectedturret=None
        
    if len(enemies)==0:
        leveldone=True
    else:
        leveldone=False
    if math.dist((mousex,mousey),(46,46))<36 and leveldone and pygame.mouse.get_pressed()[0] and not(pause) and currentspawn==None:
        level+=1
        spawn(levels[level][:levels[level][-1]],quantity=levels[level][-3],pause=levels[level][-2])
        pause=True
    if not(pygame.mouse.get_pressed()[0]):
        pause=False
    if currentpause==0 and currentspawn!=None:
        try:   
            Enemy(currentspawn)
            currentpause=spawning[-1]
            currentspawnnum+=1
            currentspawn=spawning[0][currentspawnnum]
        except IndexError:
            currentspawnnum=0
            currentspawn=spawning[0][currentspawnnum]
        
        lefttospawn-=1
        if lefttospawn<=0:
            currentspawn=None
    currentpause-=1
    for enemy in enemies:
        enemy.update()
    for turret in turrets:
        turret.update()
    for rocket in rockets:
        rocket.update()
    drawhealthbars()
    if selectedturret!=None:
        pygame.draw.circle(screen,(255,255,255,128),turret.pos,turret.range,50)
        pygame.draw.rect(screen,(230,230,230),pygame.Rect(0,960,1920,120))
    for num,explosion in enumerate(explosions):
        screen.blit(boom,(explosion[0][0]-70,explosion[0][1]-70))
        explosions[num][1]-=1
        if explosion[1]<0:
            explosions.remove(explosion)
    if mousex>1820 and mousey<60 and pygame.mouse.get_pressed()[0] and money>=50 and mouseaction!=2:
            mouseaction=2
            currentturretbeingbought='single'
            money-=50
    if mousex>1820 and mousey<110 and mousey>60 and pygame.mouse.get_pressed()[0] and money>=100 and mouseaction!=2:
            mouseaction=2
            currentturretbeingbought='double'
            money-=100
    if mousex>1820 and mousey<160 and mousey>110 and pygame.mouse.get_pressed()[0] and money>=175 and mouseaction!=2:
            mouseaction=2
            currentturretbeingbought='fast'
            money-=175
    if mousex>1820 and mousey<210 and mousey>160 and pygame.mouse.get_pressed()[0] and money>=325 and mouseaction!=2:
            mouseaction=2
            currentturretbeingbought='rocket'
            money-=325
    if mousex>1820 and mousey<260 and mousey>210 and pygame.mouse.get_pressed()[0] and money>=1200 and mouseaction!=2:
            mouseaction=2
            currentturretbeingbought='triple'
            money-=1200
    if mousex>1820 and mousey<310 and mousey>260 and pygame.mouse.get_pressed()[0] and money>=3500 and mouseaction!=2:
            mouseaction=2
            currentturretbeingbought='quadlauncher'
            money-=3500
    if mouseaction==2 and not(pygame.mouse.get_pressed()[0]):
        mouseaction-=1
    if mouseaction==1 and pygame.mouse.get_pressed()[0]:
        mouseaction-=1
    if mouseaction == 0 and not(pygame.mouse.get_pressed()[0]):
        if validturret:
            if currentturretbeingbought in ['rocket','quadlauncher']:
                RocketLauncher(mousex,mousey,currentturretbeingbought)
            else:
                Turret(mousex,mousey,currentturretbeingbought)    
            mouseaction-=1
            screen.blit(turretim,(mousex-57,mousey-40))
        else:
            mouseaction=1
    if mouseaction>-1:
        screen.blit(turretinfo[currentturretbeingbought]['image'],(mousex-57,mousey-40))
    if math.dist((1836,996),(mousex,mousey))<36 and pygame.mouse.get_pressed()[0]:
        speed+=6
        if speed>=1200:
            speed=1200
    if math.dist((1766,996),(mousex,mousey))<36 and pygame.mouse.get_pressed()[0]:
        speed-=6
        if speed<=6:
            speed=6
    screen.blit(turreticon,(1840,10))
    screen.blit(doubleturreticon,(1840,60))
    screen.blit(fastturreticon,(1840,110))
    screen.blit(rocketturreticon,(1840,160))
    screen.blit(tripleturreticon,(1840,210))
    screen.blit(quadlaunchericon,(1840,260))
    screen.blit(button,(1800,960))
    screen.blit(my_font.render(f'$ {money}',False,(0,0,0)),(10,100))
    screen.blit(my_font.render(f'Lives: {lives}',False,(0,0,0)),(900,10))
    screen.blit(my_font.render(f'Speed: {speed/60}',False,(0,0,0)),(1700,900))
    screen.blit(button,(10,10))
    screen.blit(pygame.transform.rotate(button,180),(1730,960))
    pygame.display.flip()
    clock.tick(speed)
    if lives<=0:
        raise Exception('You ran out of lives')
pygame.quit()