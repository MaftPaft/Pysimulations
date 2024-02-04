import pygame as pg
import mygame as mg
import time
import random
white,black=mg.white,mg.black
pg.init()
w,h=800,600
win=pg.display.set_mode((w,h))
fps=120
grid = []
size=20
for y in range(size,int(h),size):
    for x in range(size,int(w),size):
        grid.append(mg.SpriteClass(x,y,size,size,black,0,time.time()))
        grid[-1].n = .025
        grid[-1].originalcolor=(random.randint(0,155),random.randint(0,155),255)

mousedown=False

run=True
clock=pg.time.Clock()
while run:
    mx,my=pg.mouse.get_pos()
    mp=pg.mouse.get_pressed()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
        
    win.fill(black)
    if mp[0]:
        mousedown = True
    for g in grid:
        mouserect = pg.rect.Rect(mx-10,my-10,20,20)
        if g.speedx == 0:
            if not g.rect.colliderect(mouserect):
                g.color=black
        elif g.speedx == 1:
            if not g.rect.colliderect(mouserect):
                g.color=g.originalcolor
            ig = grid.index(g)
            sz=int(w/size)
            if time.time()-grid[ig].speedy >= grid[ig].n and ig+(sz)-1 <= len(grid)-1:
                e=random.choice([0,2])
                if grid[ig+(sz)-1].speedx != 1:
                    if grid[ig+(sz)-1].n > .025:
                        grid[ig+(sz)-1].n -= 0.015

                    grid[ig].speedx=0
                    grid[ig].color=black
                    grid[ig+(sz)-1].speedx = 1
                    grid[ig+(sz)-1].speedy=time.time()
                elif ig+(sz)-e <= len(grid)-1 and ig+(sz)-e >= 0 and ig+(sz-1)-e <= len(grid)-1 and ig+(sz-1)-e >= 0:
                    if grid[ig+(sz)-e].speedx == 0:
                        if grid[ig+(sz)-e].n > .025:
                            grid[ig+(sz)-e].n -= 0.015
                        grid[ig+(sz)-1].speedx=0
                        grid[ig+(sz)-1].color=black
                        grid[ig+(sz)-e].speedx = 1
                        grid[ig+(sz)-e].speedy=time.time()
                else:
                    if grid[ig+(sz)-1].n < .025:
                        grid[ig+(sz)-1].n += .005


        g.draw(win)

        if g.rect.colliderect(mouserect):
            g.color = (155,155,255)

        if g.rect.colliderect(mouserect) and mp[0] and g.speedx!=1:
            g.n=.025
            g.speedx=1
        if g.rect.colliderect(mouserect) and mp[2] and g.speedx==1:
            g.n=.025
            g.speedx=0

    pg.display.update()
    clock.tick(fps)
pg.quit()
