import re
import pygame as pg
import math
import random
from pygame.math import Vector2
from math import sin, cos, atan2, pi
from pyextensions.extensions import flat_floatbyK
def converter(num):
    return float(str(num).replace("(", '').replace("+0j)", ''))

def mouse_pressed():
    return pg.mouse.get_pressed()

white = (255,255,255)
black = (0,0,0)

# Classes to make Sprites
class SpriteClass(pg.sprite.Sprite):
    def __init__(self, x, y, sz, sz2, color, spedx, spedy):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pg.Surface([sz, sz2])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x-sz/2
        self.rect.y = y-sz2/2
        self.speedx = spedx
        self.speedy = spedy
        self.dx = 1
        self.dy = 1
        self.x=self.rect.x+sz/2
        self.y=self.rect.y+sz2/2
    
    
    def draw_blit(self, surface, window):
        window.blit(surface, (self.rect.x, self.rect.y))
    def draw(self,window):
        pg.draw.rect(window,self.color,self.rect)

    def rotate(self, angle):
        surf = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        surf.fill(self.color)
        rotation = pg.transform.rotate(surf, angle)
        return rotation
    def centered(self):
        self.rect.x -= self.rect.width/2
        self.rect.y -= self.rect.height/2

def colliderpie(rect, circlex, circley, circleradius):
    '''
    colliderpie(...)[0] = anglepoint
    colliderpie(...)[1] = line
    colliderpie(...)[2] = isclipped
    '''
    rectx = rect.x
    recty = rect.y
    rectwidth = rect.width
    rectheight = rect.height
    realx = rectx + (rectwidth /2)
    realy = recty + (rectheight /2)
    angle = atan2(realx-circlex, realy-circley)
    ps = (circleradius * sin(angle) + circlex, circleradius * cos(angle) + circley)
    clip = [(circlex, circley), (ps[0], ps[1])]
    clipped = rect.clipline(clip[0][0], clip[0][1], clip[1][0], clip[1][1])
    if clipped:
        return (ps, clip, clipped)
    else:
        return (ps, clip, None)

# Circle Class
class CircleClass(object):
    data={}
    def __init__(self, x, y, radius, color, window, speedxx, speedyy, dex, dey,*args):
        self.x = x
        self.y = y
        self.center = (self.x, self.y)
        self.radius = radius
        self.area = math.pi * (self.radius * self.radius)
        self.color = color
        self.speedx = speedxx
        self.speedy = speedyy
        self.dx = dex
        self.dy = dey
        self.args = list(args)


    #draw your circle class on the screen
    def draw(self, window, outlined=False, outlinedcolor=(255,255,255), outlinedwidth=2):
        pg.draw.circle(window, self.color, (self.x, self.y), self.radius)
        if outlined == True:
            pg.draw.circle(window, outlinedcolor, (self.x, self.y), self.radius + outlinedwidth, outlinedwidth)
    
    
    def rotatepoint(self, pointpositionx, pointpositiony, length, angle):
        point = Vector2(pointpositionx, pointpositiony)
        self.x = length * sin(angle) + point.x
        self.y = length * cos(angle) + point.y
    def boundaries(self,width,height):
        """
        Boundaries detection
        - rtype (List[bool]): [right, left, bottom, top] 
        """
        return [self.x > width-self.radius, self.x < self.radius, self.y > height-self.radius, self.y < self.radius]

#This is the class for adding gravity to CircleClass
class Space:
    
    def __init__(self):
        self.objs=[]
        self.static_objs=[]
        self.bounce=1
    def add(self,obj):
        self.objs.append(obj)
    def update(self,window,obj,gravity=0.0025,deltatime=1):
        if obj in self.objs:
            pg.draw.circle(window,obj.color,(obj.x,obj.y),obj.radius)
            obj.x+=obj.dx*deltatime
            obj.y+=obj.dy*deltatime
            obj.dy+=gravity
        else:
            pg.draw.circle(window,obj.color,(obj.x,obj.y),obj.radius)
    
    def add_static(self,obj):
        self.static_objs.append(obj)
    def move(self,bounce=1):
        self.bounce=bounce
        for i in range(len(self.objs)):
            # ball = self.objs[i]
            
            ball1 = self.objs[i]
            for j in range(i+1,len(self.objs)):
                ball2 = self.objs[j]
                if circleCollides(ball1.x, ball1.y, ball2.x, ball2.y, ball1.radius, ball2.radius):
                    overlap = ball1.radius + ball2.radius - math.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
                    epsilon=1e-4
                    angle=math.atan2(ball2.y-ball1.y,ball2.x-ball1.x)
                    ball1.x -= (overlap / 2 + epsilon) * math.cos(angle)
                    ball1.y -= (overlap / 2 + epsilon) * math.sin(angle)
                    ball2.x += (overlap / 2 + epsilon) * math.cos(angle)
                    ball2.y += (overlap / 2 + epsilon) * math.sin(angle)
                    collision = pg.Vector2(ball2.x-ball1.x,ball2.y-ball1.y)
                    collision.normalize_ip()
                    velocity = pg.Vector2(ball2.dx-ball2.dx,ball2.dy-ball1.dy)
                    normal = velocity.dot(collision)

                    if normal < 0:
                        e=bounce
                        j = -(1+e)*normal
                        j /= 1/ball1.radius + 1/ball2.radius
                        impulse = j*collision
                        ball1.dx -= 1 / ball1.radius * impulse.x
                        ball1.dy -= 1 / ball1.radius * impulse.y
                        ball2.dx += 1 / ball2.radius * impulse.x
                        ball2.dy += 1 / ball2.radius * impulse.y

                    # ball1.dx*=0.9
                    # ball1.dy*=0.9
                        ball1.dx*=0.9
                        ball1.dy*=0.9
            # if self.static_objs:
            for s in self.static_objs:
                ball = self.objs[i]
                if circleCollides(s.x,s.y,ball.x,ball.y,s.radius,ball.radius):
                    overlap = ball.radius + s.radius - math.sqrt((ball.x - s.x) ** 2 + (ball.y - s.y) ** 2)
                    epsilon=1e-4
                    angle=math.atan2(s.y-ball.y,s.x-ball.x)
                    ball.x -= (overlap) * math.cos(angle)
                    ball.y -= (overlap) * math.sin(angle)
                    collision = pg.Vector2(s.x-ball.x,s.y-ball.y)
                    collision.normalize_ip()
                    velocity = pg.Vector2(0,-ball.dy)
                    normal = velocity.dot(collision)

                    if normal < 0:
                    
                        e=bounce
                        j = -(1+e)*normal
                        j /= 1/ball.radius*2
                        impulse = j*collision
                        ball.dx -= 1 / ball.radius * impulse.x
                        ball.dy -= 1 / ball.radius * impulse.y
                    # ball.dx*=0.9
                    # ball.dy*=0.9
    def boundaries(self,width,height,obj):
        # velocity = pg.Vector2(0,-ball.dy)
        # normal = velocity.dot(collision)

        # if normal < 0:
        
        #     e=bounce
        #     j = -(1+e)*normal
        #     j /= 1/ball.radius*2
        #     impulse = j*collision
        #     ball.dx -= 1 / ball.radius * impulse.x
        #     ball.dy -= 1 / ball.radius * impulse.y
        
        collision = pg.Vector2(0,obj.y).normalize()
        velocity = pg.Vector2(0,-obj.dy)
        normal = velocity.dot(collision)
        if normal < 0:
            e=self.bounce
            j = -(1+e)*normal
            j /= 1/obj.radius*2
            impulse = j*collision
            if obj.y > height-obj.radius:
                obj.y = height-obj.radius-1
                obj.dy-= 1/obj.radius*impulse.y
            if obj.y < obj.radius:
                obj.y = obj.radius+1
                obj.dy += 1/obj.radius*impulse.y
        collision = pg.Vector2(obj.x,0).normalize()
        velocity = pg.Vector2(-obj.dx,0)
        normal = velocity.dot(collision)
        e=self.bounce
        j = -(1+e)*normal
        j /= 1/obj.radius*2
        impulse = j*collision
        if obj.x > width-obj.radius:
            obj.x = width-obj.radius-1
            obj.dx-=1/obj.radius*impulse.x

        if obj.x < obj.radius:
            obj.x = obj.radius+1
            obj.dx -= 1/obj.radius*impulse.x

        if obj.y > height-obj.radius:
            obj.y=height-obj.radius
            # obj.dy*=0.9
        if obj.y < obj.radius:
            obj.y = obj.radius
            # obj.dy*=0.9
        if obj.x > width-obj.radius:
            obj.x=width-obj.radius
            # obj.dx*=0.9
        if obj.x < obj.radius:
            obj.x=obj.radius
            # obj.dx*=0.9


                    
    


class Slider:
    def __init__(self,x,y,width,height,initial_val,min,max,container_color=(155,155,155),button_color=(255,255,255)):
        self.x,self.y=x,y
        self.width=width
        self.height=height
        self.container_color=container_color
        self.button_color=button_color

        self.left=self.x-(width/2)
        self.right=self.x+(width/2)
        self.top=self.y-(height/2)
        self.bottom=self.y+(height/2)

        self.min=min
        self.max=max
        self.initial_val=(self.right-self.left)*initial_val # percentage
        
        self.container_rect = pg.Rect(self.left,self.top,self.width,self.height)
        self.button_rect = pg.Rect(self.left+self.initial_val - 5, self.top, 10, self.height)
        self.clipped = False
    
    def move_slider(self,mouse_pos):
        if self.container_rect.collidepoint(mouse_pos):
            self.clipped = True
        if pg.mouse.get_pressed()[0] and mouse_pos[0] <= self.container_rect.width+self.container_rect.x and mouse_pos[0] >= self.container_rect.x:
            if self.clipped:
                self.button_rect.centerx = mouse_pos[0]
        else:
            self.clipped=False
    def reset_button(self):
        self.button_rect.x=self.left+self.initial_val-5
        self.button_rect.y=self.top

    def render(self,window):
        pg.draw.rect(window,self.container_color,self.container_rect)
        pg.draw.rect(window,self.button_color,self.button_rect)
    def get_value(self):
        val_range = self.right-self.left
        button_val = self.button_rect.centerx - self.left
        return (button_val/val_range)*(self.max-self.min)
    def value_display(self,window,color,fontsize,offsetval=0):
        text=str(flat_floatbyK(self.get_value()+offsetval,3))
        pygame_text(self.right-(fontsize*len(text)/2),self.y,"",fontsize,color,text).update(window)

#text on screen
class pygame_text:
    def __init__(self,x,y,font,fontsize,color,text):
        self.x,self.y=x,y
        self.font=font
        self.fontsize=fontsize
        self.color=color
        self.text=text
        self.size=(0,0)
        self.rect=self.get_rect()
        
    def update(self,window):
        font = pg.font.SysFont(self.font, self.fontsize)
        self.size = font.size(self.text)
        surface = font.render(self.text,False,self.color)
        window.blit(surface,(self.x,self.y))
        self.rect = self.get_rect()
    def get_rect(self):
        return pg.rect.Rect(self.x,self.y,self.size[0],self.size[1])

class particle:
    def __init__(self,x,y,color,span,velx,vely,*mod):
        self.x=x
        self.y=y
        self.color=color
        self.dx=velx
        self.dy=vely
        self.span=span
        self.mod = list(mod)
        self.t=[]
    def move(self,aging=0.05,dt=1):
        """
        Parameter: 
        - dt (deltatime)
            
            deltatime is set to 1, which does not affect the code at all.
            get deltatime: fps/(1/clock.get_fps())
            
        rtype:
        - None
        
        Use the aging function for the particle to die
        Remove this item in a list:
            if self.span <= 0:
                remove from list
        """
        self.x += self.dx*dt
        self.y += self.dy*dt
        for i in range(len(self.mod)):
            if i%2==0:
                self.dx += self.mod[i]
            else:
                self.dy += self.mod[i]
        self.span -= aging*dt
        
    def boundaries(self,w,h):
        if self.x >= w-self.span or self.x <= self.span:
            self.dx *= -0.99
            if self.x > w-self.span:
                self.x = w-self.span
            elif self.x < self.span:
                self.x = self.span
                
        if self.y >= h-self.span or self.y <= self.span:
            self.dy *= -0.99
            if self.y > h-self.span:
                self.y = h-self.span
            elif self.y < self.span:
                self.y = self.span



    def trace(self,size=random.randint(1,5)):
        """
        to draw the particles
        """
        self.t.append([pg.Vector2(self.x,self.y),size])
    def draw(self,window,dt=1):
        """
        if size is None then size is lifespan
        - drawing a line from trace
        """
        if self.t:
            for i in range(1, len(self.t)):
                pg.draw.line(window,self.color,(self.t[i-1][0].x,self.t[i-1][0].y),(self.t[i][0].x,self.t[i][0].y),int(self.t[i][1]))
                if self.t[i][1] >= 0:
                    self.t[i][1] -= 0.1*dt
        else:
            pg.draw.circle(window,self.color,(self.x,self.y),self.span)
                


        

        

# collision detection (only for CircleSprites)
def circleCollides(x1, y1, x2, y2, radius1, radius2):
    distance = math.hypot(x1 - x2, y1 - y2)
    collided = distance <= radius1 + radius2
    return collided == True
    
def intersect_line_line(P0, P1, Q0, Q1):  
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        return None
    t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
    u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return P1[0] * t + P0[0] * (1-t), P1[1] * t + P0[1] * (1-t)
    return None



num = 0
rot = 1
off = 1
ron = (200, random.randint(0, 240), 50)
getVrotationx = []
getVrotationy = []

class points:
    def __init__(self, targetspos, targetsradius, radius=5, numV=0, rotatedV=90):
        global rot, off
        super().__init__()
        self.radius = radius
        self.speed = 0
        self.pos = Vector2(targetspos)
        self.front = Vector2(0, targetsradius)
        self.left = self.front.rotate(90)
        self.right = self.front.rotate(-90)
        self.sidev = []
        self.rotatedV = rotatedV
        for i in range(numV):
            ron = (240, random.randint(0, 240), 50)
            self.sidev.append(self.front.rotate(rotatedV))
            self.sidev[0] = self.front.rotate(rotatedV)
            if rot <= len(self.sidev) - 1 and len(self.sidev) > 0:
                self.sidev[rot] = self.sidev[rot - 1].rotate(rotatedV)
                rot += 1
            else:
                rot = 1
            for s in self.sidev:
                for others in self.sidev:
                    if circleCollides(self.pos[0]+s[0], self.pos[1]+s[1], self.pos[0]+others[0], self.pos[1]+others[1], self.radius, self.radius):
                        others.rotate_ip(rotatedV / off)
                        s.rotate_ip(rotatedV / off)
                    
                    if circleCollides(self.pos[0]+s[0], self.pos[1]+s[1], self.pos[0]+others[0], self.pos[1]+others[1], self.radius, self.radius) and s[1] >= 50 and s[0] <= 0 or circleCollides(self.pos[0]+s[0], self.pos[1]+s[1], self.pos[0]+others[0], self.pos[1]+others[1], self.radius, self.radius) and s[1] <= -50:
                        s.rotate_ip(rotatedV / off)
                        off += numV / 1
                
                
        for s in self.sidev:
            getVrotationx.append(s[0])
            getVrotationy.append(s[1])
        
    def rotate(self):
        self.front.rotate_ip(self.speed)
        for s in self.sidev:
            s.rotate_ip(self.speed)
    
    
    def vector(self, Vector, choosexy):
        return self.sidev[Vector][choosexy]
    
    
    def drawpoints(self, window, color=(255, 0, 0)):
        global num
        pg.draw.circle(window, color, list(map(int, self.pos+self.front)), self.radius)
        pg.draw.line(window, color, self.pos, self.pos+self.front, 2)
        
        for s in self.sidev:
            pg.draw.circle(window, color, list(map(int, self.pos+s)), self.radius)
            pg.draw.line(window, ron, self.pos, self.pos+s, 2)

class pgimage:
    def __init__(self, x, y, stringimage):
        self.image = pg.image.load(stringimage)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
    def draw(self, window, surface):
        window.blit(surface, (self.x, self.y))



# Colliding the sides of the window
def col_right(objectx, window_width):
    collided = objectx >= window_width
    return collided == True

def col_bottom(objecty, window_height):
    collided = objecty >= window_height
    return collided == True

def col_left(objectx, left=0):
    collided = objectx <= left
    return collided == True
    
def col_top(objecty, top=0):
    collided = objecty <= top
    return collided == True

grouping = []
def grouped(*group):
    grouping = []
    grouping.append(group)
    res = str(group)[1:-1]
    return res

def screen(width, height):
    return pg.display.set_mode((width, height))
    
