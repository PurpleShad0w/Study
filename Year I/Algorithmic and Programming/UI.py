import pygame 
import random
import pysnooper

pygame.init()
smalltext = pygame.font.Font("Roboto-Regular.ttf",12)
mediumtext = pygame.font.Font("Roboto-Regular.ttf",20)
largetext = pygame.font.Font("Roboto-Regular.ttf",30)
width = 800
height = 600
size = 50
colors = [(255,0,0),(0,255,0),(0,0,255),(255,165,0),(143,0,255),(240,195,0)] #red,Green,Blue,Orange,purple,yellow.
lred = (200,0,0)
red = (255,0,0)
green = (102,204,0)
white = (255,255,255)
black = (0,0,0)
nplayers = 1
nshapes = 6
ncolors = 6
nidentical = 3
checkp1,checkp2,checkp3,checkp4 = True,False,False,False
checkc1,checkc2,checkc3,checkc4 = False,False,False,True
checks1,checks2,checks3,checks4 = False,False,False,True
checki1,checki2,checki3,checki4 = False,True,False,False

pos = [width//2,height-2*size]


screen = pygame.display.set_mode((width,height))

def text_objects(text, font):
    Surface = font.render(text,True,white)
    return Surface, Surface.get_rect()

def button(msg,x,y,w,h,i,a,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,a,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))

    SmallText = pygame.font.Font("NotoSansKR-Regular.otf",30)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonplayers1(msg,x,y,w,h,i,a,action):
    global checkp1,checkp2,checkp3,checkp4,nplayers
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checkp1,checkp2,checkp3,checkp4,nplayers = True,False,False,False,1
    if checkp1 == True and action == 1:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)      

def buttonplayers2(msg,x,y,w,h,i,a,action):
    global checkp1,checkp2,checkp3,checkp4,nplayers
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checkp1,checkp2,checkp3,checkp4,nplayers = False,True,False,False,2
    if checkp2 == True and action == 2:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonplayers3(msg,x,y,w,h,i,a,action):
    global checkp1,checkp2,checkp3,checkp4,nplayers
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checkp1,checkp2,checkp3,checkp4,nplayers = False,False,True,False,3
    if checkp3 == True and action == 3:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonplayers4(msg,x,y,w,h,i,a,action):
    global checkp1,checkp2,checkp3,checkp4,nplayers
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checkp1,checkp2,checkp3,checkp4,nplayers = False,False,False,True,4
    if checkp4 == True and action == 4:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttoncolors1(msg,x,y,w,h,i,a,action):
    global checkc1,checkc2,checkc3,checkc4,ncolors
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checkc1,checkc2,checkc3,checkc4,ncolors = True,False,False,False,3
    if checkc1 == True and action == 3:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttoncolors2(msg,x,y,w,h,i,a,action):
    global checkc1,checkc2,checkc3,checkc4,ncolors
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checkc1,checkc2,checkc3,checkc4,ncolors = False,True,False,False,4
    if checkc2 == True and action == 4:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttoncolors3(msg,x,y,w,h,i,a,action):
    global checkc1,checkc2,checkc3,checkc4,ncolors
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checkc1,checkc2,checkc3,checkc4,ncolors = False,False,True,False,5
    if checkc3 == True and action == 5:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttoncolors4(msg,x,y,w,h,i,a,action):
    global checkc1,checkc2,checkc3,checkc4,ncolors
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checkc1,checkc2,checkc3,checkc4,ncolors = False,False,False,True,6
    if checkc4 == True and action == 6:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonshapes1(msg,x,y,w,h,i,a,action):
    global checks1,checks2,checks3,checks4,nshapes
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checks1,checks2,checks3,checks4,nshapes = True,False,False,False,3
    if checks1 == True and action == 3:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonshapes2(msg,x,y,w,h,i,a,action):
    global checks1,checks2,checks3,checks4,nshapes
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checks1,checks2,checks3,checks4,nshapes = False,True,False,False,4
    if checks2 == True and action == 4:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonshapes3(msg,x,y,w,h,i,a,action):
    global checks1,checks2,checks3,checks4,nshapes
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checks1,checks2,checks3,checks4,nshapes = False,False,True,False,5
    if checks3 == True and action == 5:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)    

def buttonshapes4(msg,x,y,w,h,i,a,action):
    global checks1,checks2,checks3,checks4,nshapes
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checks1,checks2,checks3,checks4,nshapes = False,False,False,True,6
    if checks4 == True and action == 6:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonidentical1(msg,x,y,w,h,i,a,action):
    global checki1,checki2,checki3,checki4,nidentical
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checki1,checki2,checki3,checki4,nidentical = True,False,False,False,1
    if checki1 == True and action == 1:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonidentical2(msg,x,y,w,h,i,a,action):
    global checki1,checki2,checki3,checki4,nidentical
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checki1,checki2,checki3,checki4,nidentical = False,True,False,False,2
    if checki2 == True and action == 2:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def buttonidentical3(msg,x,y,w,h,i,a,action):
    global checki1,checki2,checki3,checki4,nidentical
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
            checki1,checki2,checki3,checki4,nidentical = False,False,True,False,3
    if checki3 == True and action == 3:
        pygame.draw.rect(screen,a,(x,y,w,h))
    else:
        pygame.draw.rect(screen,i,(x,y,w,h))
    
    SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
    Surf,Rect = text_objects(msg,SmallText)
    Rect.center = ((x + (w/2)),(y + (h/2)))
    screen.blit(Surf,Rect)

def Main_menu():
    intro = True
    while intro == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(black)
        LargeText = pygame.font.Font("PlayfairDisplay-VariableFont_wght.ttf",80)
        Surf,Rect = text_objects("Qwirkle",LargeText)
        Rect.center = ((width/2),(height/4))
        screen.blit(Surf,Rect)
        button("Quit ?",325,300,150,50,red,lred,quit)
        button("Play !",325,200,150,50,red,lred,parameters)
        pygame.display.update()

def parameters():
    intro = True
    while intro == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(black)
        LargeText = pygame.font.Font("Roboto-Regular.ttf",40)
        mediumtext = pygame.font.Font("Roboto-Regular.ttf",30)
        Surf,Rect = text_objects("Parameters",LargeText)
        nbplayers,Rect1 = text_objects("Number of players :",mediumtext)
        nbcolors,Rect2 = text_objects("Number of colors :",mediumtext)
        nbshapes,Rect3 = text_objects("Number of shapes :",mediumtext)
        nbsimilar,Rect4 = text_objects("number of identical tiles :",mediumtext)  
        Rect.center = ((width/2),(height/10))
        Rect1.center = ((width/2),(height/6))
        Rect2.center = ((width/2),(height/3))
        Rect3.center = ((width/2),(height/2))
        Rect4.center = ((width/2),(height/1.5))
        screen.blit(Surf,Rect)
        screen.blit(nbplayers,Rect1)
        screen.blit(nbcolors,Rect2)
        screen.blit(nbshapes,Rect3)
        screen.blit(nbsimilar,Rect4)
        buttonplayers1("1",320,130,25,25,lred,green,1)
        buttonplayers2("2",370,130,25,25,lred,green,2)
        buttonplayers3("3",420,130,25,25,lred,green,3)
        buttonplayers4("4",470,130,25,25,lred,green,4)

        SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
        Surf,Rect = text_objects(str(nplayers),SmallText)
        Rect.center = ((600),(100))
        screen.blit(Surf,Rect)

        buttoncolors1("3",320,230,25,25,lred,green,3)
        buttoncolors2("4",370,230,25,25,lred,green,4)
        buttoncolors3("5",420,230,25,25,lred,green,5)
        buttoncolors4("6",470,230,25,25,lred,green,6)

        SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
        Surf,Rect = text_objects(str(ncolors),SmallText)
        Rect.center = ((600),(200))
        screen.blit(Surf,Rect)

        buttonshapes1("3",320,330,25,25,lred,green,3)
        buttonshapes2("4",370,330,25,25,lred,green,4)
        buttonshapes3("5",420,330,25,25,lred,green,5)
        buttonshapes4("6",470,330,25,25,lred,green,6)

        SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
        Surf,Rect = text_objects(str(nshapes),SmallText)
        Rect.center = ((600),(300))
        screen.blit(Surf,Rect)

        buttonidentical1("1",345,430,25,25,lred,green,1)
        buttonidentical2("2",395,430,25,25,lred,green,2)
        buttonidentical3("3",445,430,25,25,lred,green,3)

        SmallText = pygame.font.Font("Roboto-Regular.ttf",20)
        Surf,Rect = text_objects(str(nidentical),SmallText)
        Rect.center = ((600),(400))
        screen.blit(Surf,Rect)

        button("Launch",325,500,150,50,lred,red,quit)

        pygame.display.update()
        

Main_menu()
