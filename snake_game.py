import pygame as pg
from math import *
from random import randint


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

class SpriteClass(pg.sprite.Sprite):
    def __init__(self, x, y, sz, sz2, color):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pg.Surface([sz, sz2])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x-sz/2
        self.rect.y = y-sz2/2
    
    
    def draw(self,window):
        pg.draw.rect(window,self.color,self.rect)


pg.init()

def main():
    white,black = (255,255,255),(0,0,0)
    w,h=900,700
    win=pg.display.set_mode((w,h))
    fps=8
    grid=[]
    w,h=800,600

    snakes = [SpriteClass(w/2,h/2,25,25,white)]
    i=0
    add=3
    for y in range(int(h/snakes[0].rect.h)+add):
        for x in range(int(w/snakes[0].rect.w)+add):
            c = (100,200,100)
            if i%2==0:
                c = (155,255,155)
            grid.append(SpriteClass(x*snakes[0].rect.w+25,y*snakes[0].rect.h+25,snakes[0].rect.w-5,snakes[0].rect.h-5,c))
            i+=1

    bordercolor=(255,255,255)
    for n in range(int(len(grid)/25)-2):
        grid[n].color = bordercolor
    for n in range(0,int(len(grid)),35):
        grid[n].color=bordercolor
    for n in range(34,int(len(grid)),35):
        grid[n].color=bordercolor
    for n in range(len(grid)-34,int(len(grid))):
        grid[n].color = bordercolor
    n=int(len(grid)/2)
    gplace=randint(0,len(grid)-1)
    points = 0
    foodsize=17.5
    foodcolor=(200,15,15)
    food = pg.rect.Rect(grid[gplace].rect.x+1.75,grid[gplace].rect.y+1.75,foodsize,foodsize)
    while grid[gplace].color == bordercolor:
        gplace=randint(0,len(grid)-1)
        food.x=grid[gplace].rect.x+1.75
        food.y=grid[gplace].rect.y+1.75
    direction="R"
    length=2
    run=True
    clock=pg.time.Clock()
    close = False
    while run:
        x,y = grid[n].rect.x-(snakes[0].rect.w/10),grid[n].rect.y-(snakes[0].rect.h/10)
        snakes.insert(0,SpriteClass(x,y,snakes[0].rect.w,snakes[0].rect.h,snakes[0].color))
        if len(snakes) > length:
            snakes.pop()
        for i in pg.event.get():
            if i.type == pg.QUIT:
                close = True
                run=False
            if i.type == pg.KEYDOWN:
                if i.key == pg.K_UP and direction != "D" and direction != "U":
                    direction = "U"
                if i.key == pg.K_RIGHT and direction != "L" and direction != "R":
                    direction = "R"
                if i.key == pg.K_LEFT and direction != "R" and direction != "L":
                    direction = "L"
                if i.key == pg.K_DOWN and direction != "U" and direction != "D":
                    direction = "D"
                
        win.fill((0,155,0))
        for g in grid:
            g.draw(win)
            if pg.rect.Rect(x,y,snakes[0].rect.w,snakes[0].rect.h).colliderect(g.rect) and g.color == bordercolor:
                print('BORDER COLLISION')
                run=False

        snakes[0].rect.x,snakes[0].rect.y=x,y
        if direction == "R":
            n+=1
        if direction == "L":
            n-=1
        if direction == "U":
            n -= int(w / snakes[0].rect.w)+add
        if direction == "D":
            n += int(w / snakes[0].rect.w)+add
        
        if snakes[0].rect.colliderect(food):
            gplace=randint(0,len(grid)-1)
            food.x=grid[gplace].rect.x+1.75
            food.y=grid[gplace].rect.y+1.75
            while grid[gplace].color == bordercolor:
                gplace=randint(0,len(grid)-1)
                food.x=grid[gplace].rect.x+1.75
                food.y=grid[gplace].rect.y+1.75
            points+=1
            length+=1
            fps+=1



        for i, s in enumerate(snakes):
            pg.draw.rect(win,black,s.rect,5,5,5,5,5,5)
            pg.draw.rect(win,white,pg.rect.Rect(s.rect.x+3,s.rect.y+3,s.rect.w-7.5,s.rect.h-7.5))
            
            for j in range(i+1,len(snakes)):
                if j!= 0 and snakes[0].rect.colliderect(snakes[j]):
                    print("Your tail got tangled :(\n better luck next time!")
                    run=False

        pg.draw.rect(win,foodcolor,food)
        pg.draw.rect(win,(255,155,155),pg.rect.Rect(food.x-2.5,food.y-2.5,food.w+5,food.h+5),3,3,3,3,3,3)
            
        pg.display.update()
        clock.tick(fps)
        


    run=True
    while run and close == False:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                run=False
            if i.type == pg.KEYUP:
                if i.key == pg.K_r:
                    run=False
                    print('restarting')
                    main()
        win.fill((100,200,100))

        text = pygame_text(w/2,h/2,"",int((w+h)/8),(155,255,155),f"POINTS:{points}")
        text.x=w/2-(len(text.text)*int((w+h)/32))
        text.update(win)

        pygame_text(0,0,"",75,(200,255,200),"press 'r' to restart").update(win)

        pg.display.update()
        clock.tick(120)
    pg.quit()
if __name__ == '__main__':
    main()
