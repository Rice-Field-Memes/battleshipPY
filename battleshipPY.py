from sys import stdout

import pyglet
from pyglet.window import key, mouse

from Ship import Pos, Ship
from Cursor import Cursor
from Game import Game

screenw, screenh = 1280,720
window = pyglet.window.Window(screenw,screenh)

debugLabel = pyglet.text.Label('DEBUG MODE ENABLED',
                          font_name='Times New Roman',
                          font_size=36,
                          color=(128, 128, 128, 255),
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

grid = pyglet.resource.image('images/screen720.png')

piv1 = pyglet.resource.image('images/1piv.png')
piv1.anchor_x,piv1.anchor_y=32,32

curs1 = pyglet.resource.image('images/1curs.png')
curs1.anchor_x,curs1.anchor_y=32,32

cursSprite = pyglet.sprite.Sprite(img=curs1)
cursSprite.opacity = 192

pivotSprite = pyglet.sprite.Sprite(img=piv1)
pivotSprite.opacity = 192

shipBatch = pyglet.graphics.Batch()
grid_offx, grid_offy = 96,48

coordP = lambda xy : (xy[0]*64+grid_offx, xy[1]*64+grid_offy)
coordX = lambda x : x*64+grid_offx
coordY = lambda y : y*64+grid_offy
posC = lambda ab: (int((ab[0]-grid_offx)/64), int((ab[1]-grid_offy)/64))

cursor = Cursor()
carrier = Ship(5)
battleship = Ship(4,0,2)
cruiser = Ship(3,0,4)
submarine = Ship(3,0,6)
destroyer = Ship(2,0,8)

ships = [carrier,battleship,cruiser,submarine,destroyer]

for z in ships: z.sprite.batch = shipBatch
game = Game()

#input function
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        #space key logic, switching between ghost and non
        if game.state==0:
            if cursor.sel==-1:
                for i,s in enumerate(ships):
                    if (cursor.x,cursor.y) in s.allCoords():
                        s.cursOnLine = s.allCoords().index((cursor.x,cursor.y))
                        s.gx,s.gy = s.x,s.y
                        s.grot = s.rotate
                        s.ghost = True
                        cursor.sel = i
                        s.sprite.visible = False
                        break
            else:
                aCrds = [e.gCoords() for e in ships if e!=ships[cursor.sel]]
                if not set(ships[cursor.sel].gCoords()).intersection([x for x in aCrds for x in x]):
        #            for c in ships[current.sel].gCoords(): if c in 
                    ships[cursor.sel].x,ships[cursor.sel].y = ships[cursor.sel].gx,ships[cursor.sel].gy
                    ships[cursor.sel].rotate = ships[cursor.sel].grot
                    #cursor.x,cursor.y = des.gx,des.gy
                    ships[cursor.sel].ghost = False
                    ships[cursor.sel].sprite.visible=True
                    game.debug = False
                    cursor.sel = -1
        elif game.state==1:
            game.shoot(cursor.x,cursor.y)
    elif symbol == key.ENTER:
        if cursor.sel==-1 and game.state==0:
            game.state = 1
            game.setGrid(ships)
    elif symbol in [key.W, key.UP]:
        #leaving just in case
        #if not des.ghost: cursor.y = (cursor.y+1)%10
        cursor.y+=1
        if cursor.sel!=-1: ships[cursor.sel].gy+=1
    elif symbol in [key.A, key.LEFT]:
        cursor.x-=1
        if cursor.sel!=-1: ships[cursor.sel].gx-=1
    elif symbol in [key.S, key.DOWN]:
        cursor.y-=1
        if cursor.sel!=-1: ships[cursor.sel].gy-=1
    elif symbol in [key.D, key.RIGHT]:
        cursor.x+=1
        if cursor.sel!=-1: ships[cursor.sel].gx+=1
    elif symbol in [key.Q,key.E] and cursor.sel!=-1:
        #rotate
        if symbol==key.Q: ships[cursor.sel].grot = (ships[cursor.sel].grot-1)%4
        elif symbol==key.E: ships[cursor.sel].grot = (ships[cursor.sel].grot+1)%4
        #moving pivot to make cursor not move
        if ships[cursor.sel].grot==1: ships[cursor.sel].setGP(cursor.x+ships[cursor.sel].cursOnLine,cursor.y)
        elif ships[cursor.sel].grot==3: ships[cursor.sel].setGP(cursor.x-ships[cursor.sel].cursOnLine,cursor.y)
        elif ships[cursor.sel].grot==0: ships[cursor.sel].setGP(cursor.x,cursor.y+ships[cursor.sel].cursOnLine)
        elif ships[cursor.sel].grot==2: ships[cursor.sel].setGP(cursor.x,cursor.y-ships[cursor.sel].cursOnLine)
    if symbol == key.Z and cursor.sel != -1:
        game.debug = not game.debug
    [s.update() for s in ships]
    if cursor.sel!=-1:
        des = ships[cursor.sel]
        if des.grot == 3:
            des.gx -= max(0, des.gx+des.len-10)
            #cursor.x -= max(0, des.gx+des.len-10)
        elif des.grot == 2:
            des.gy -= max(0, des.gy+des.len-10)
            #cursor.y -= max(0, des.gy+des.len-10)
        elif des.grot == 0:
            des.gy -= min(0, des.gy-des.len+1)
            #cursor.y -= min(0, des.gy-des.len+1)
        elif des.grot == 1:
            des.gx -= min(0, des.gx-des.len+1)
            #cursor.x -= min(0, des.gx-des.len+1)

        des.gx = max(0, min(9,des.gx))
        des.gy = max(0, min(9,des.gy))
        cursor.x,cursor.y = des.gCoords()[des.cursOnLine]

        des.ghostSprite.update(coordX(des.gx),coordY(des.gy),rotation=(des.grot*90+90)%360)
        pivotSprite.update(coordX(cursor.x),coordY(cursor.y))
    else:
        cursor.x%=10
        cursor.y%=10
    cursSprite.update(coordX(cursor.x),coordY(cursor.y))
#    print("{0}, {1}".format(cursor.x,cursor.y))
#    print(des.cursOnLine)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    pass

#drawing function
@window.event
def on_draw():
    window.clear()
    grid.blit(0, 0)
    shipBatch.draw()
    if game.state==0:
        game.infoPlaceSprite.draw()
        if cursor.sel!=-1:
            ships[cursor.sel].ghostSprite.draw()
            pivotSprite.draw()
        else:
            #shipSprite.draw()
            cursSprite.draw()
    else:
        cursSprite.draw()
        game.shotBatch.draw()
        if game.turn%2==0: game.infoYtSprite.draw()
        else: game.infoEtSprite.draw()
    if game.debug: debugLabel.draw()

if __name__ == "__main__":
    [s.update() for s in ships]
    cursSprite.update(coordX(cursor.x),coordY(cursor.y))
    pyglet.app.run()