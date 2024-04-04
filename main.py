import pygame
import math
import numpy

pygame.init()
width, height = 1920, 1020
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("AZ-kviz")

font = pygame.font.Font(None, 40)
pismeno = numpy.array(['Š', 'T', 'U', 'V', 'W', 'Z', 'Ž',
                       'N', 'O', 'P', 'R', 'Ř', 'S',
                       'I', 'J', 'K', 'L', 'M',
                       'F', 'G', 'H', 'Q',
                       'Č', 'D', 'E',
                       'B', 'C',
                       'A'], dtype=numpy.str_)
pozice = numpy.array([[780, 660], [840, 660], [900, 660], [960, 660], [1020, 660], [1080, 660], [1140, 660],
                      [810, 610], [870, 610], [930, 610], [990, 610], [1050, 610], [1110, 610],
                      [840, 560], [900, 560], [960, 560], [1020, 560], [1080, 560],
                      [870, 510], [930, 510], [990, 510], [1050, 510],
                      [900, 460], [960, 460], [1020, 460],
                      [930, 410], [990, 410],
                      [960, 360]], dtype=object)
spodni = [0, 1, 2, 3, 4, 5, 6]
leva = [0, 7, 13, 18, 22, 25, 27]
prava = [6, 12, 17, 21, 24, 26, 27]
barvy = numpy.array(['white', 'white', 'white', 'white', 'white', 'white', 'white',
                       'white', 'white', 'white', 'white', 'white', 'white',
                       'white', 'white', 'white', 'white', 'white',
                       'white', 'white', 'white', 'white',
                       'white', 'white', 'white',
                       'white', 'white',
                       'white'], dtype=numpy.str_)
seznam_otazek = numpy.array(['a', 'a', 'a', 'a', 'a', 'a', 'a',
                       'a', 'a', 'a', 'a', 'a', 'a',
                       'a', 'a', 'a', 'a', 'a',
                       'a', 'a', 'a', 'a',
                       'a', 'a', 'a',
                       'a', 'a',
                       'jaka je nejlepsi znacka aut?'], dtype=numpy.str_)
seznam_otazek_cerne = numpy.array(['je audi nejlepsi znacka aut? ano nebo ne?', 'b', 'b', 'b', 'b', 'b', 'b'], dtype=numpy.str_)
seznam_odpovedi = numpy.array(['a', 'a', 'a', 'a', 'a', 'a', 'a',
                       'a', 'a', 'a', 'a', 'a', 'a',
                       'a', 'a', 'a', 'a', 'a',
                       'a', 'a', 'a', 'a',
                       'a', 'a', 'a',
                       'a', 'a',
                       'audi'], dtype=numpy.str_)
seznam_odpovedi_cerne = numpy.array(['ano', 'b', 'b', 'b', 'b', 'b', 'b'], dtype=numpy.str_)

poradi_cerne = 0
poradi_hrac = 'hraje červená'
stav = 1
odpoved = ""

def sestiuhelnik(surface, color, center):
    vertices = []
    side_length = 30
    for i in range(6):
        angle_rad = math.radians(60 + 60 * i +90)
        x = center[0] + side_length * math.cos(angle_rad)
        y = center[1] + side_length * math.sin(angle_rad)
        vertices.append((x, y))
    pygame.draw.polygon(surface, color, vertices)
def uvnitr_sestiuhelniku(point_mys, center):
    x_mys, y_mys = point_mys
    for i in range(len(center)):
        x_max = center[i, 0]+25
        x_min = center[i, 0]-25
        y_max = center[i, 1]+20
        y_min = center[i, 1]-20
        if x_mys <= x_max and x_mys >= x_min and y_mys <= y_max and y_mys >= y_min:
            return i
def vypis_desky(hrac):
    screen.fill("blue")
    for i in range(len(pozice)):
        sestiuhelnik(screen, str(barvy[i]), tuple(pozice[i]))
    for i in range(len(pozice)):
        text_surface = font.render(str(pismeno[i]), True, 'black')
        screen.blit(text_surface,tuple(pozice[i]-9))
    text_surface = font.render(str(hrac), True, 'black')
    screen.blit(text_surface, (875, 290))
def kontrola_strany(strana, pole, barva):
    obsazene = []
    for i in range(len(strana)):
        if str(pole[strana[i]]) == str(barva):
            obsazene.append(strana[i])
    return obsazene
def kontrola_trojice(barva):
    podminka_trojice = False
    nejkratsi = []
    spodniOK = kontrola_strany(spodni, barvy, barva)
    levaOK = kontrola_strany(leva, barvy, barva)
    pravaOK = kontrola_strany(prava, barvy, barva)
    if len(spodniOK) != 0 and len(pravaOK) != 0 and len(levaOK) != 0:
        podminka_trojice = True
        nejkratsi = spodniOK
        if len(nejkratsi) > len(levaOK):
            nejkratsi = levaOK
        if len(nejkratsi) > len(pravaOK):
            nejkratsi = pravaOK
    return podminka_trojice, nejkratsi
def vyherni_kontrola_strany(strana, pozice_spojenych):
    ok = False
    for i in range(len(pozice_spojenych)):
        if pozice_spojenych[i] in strana:
            ok = True
            break
    return ok
def vyherni_kontrola_trojice(pozice_spojenych):
    if vyherni_kontrola_strany(spodni, pozice_spojenych) == True and vyherni_kontrola_strany(leva, pozice_spojenych) == True and vyherni_kontrola_strany(prava, pozice_spojenych) == True:
        return True
def souradnice_podle_barev(souradnice, barvy, barva):
    souradnice_obsazene = numpy.array([0,0], dtype=object)
    pozice_obsazene = []
    for i in range(len(souradnice)):
        if str(barvy[i]) == str(barva):
            pozice_obsazene.append(i)
            souradnice_obsazene = numpy.vstack((souradnice_obsazene, numpy.array(souradnice[i])))
    souradnice_obsazene = numpy.delete(souradnice_obsazene, 0, axis=0)
    return souradnice_obsazene, pozice_obsazene
def podminka_spojeni(nejmensi, barva):
    vyhra = False
    souradnice_obsazenych, pozice_obsazene = souradnice_podle_barev(pozice, barvy, barva)
    for i in range(len(nejmensi)):
        napojene = [nejmensi[i]]
        j=0
        while j < len(napojene):
            x_max = pozice[napojene[j], 0]+70
            x_min = pozice[napojene[j], 0]-70
            y_max = pozice[napojene[j], 1]+60
            y_min = pozice[napojene[j], 1]-60
            for k in range(len(pozice_obsazene)):
                if pozice_obsazene[k] not in napojene and souradnice_obsazenych[k, 0] < x_max and souradnice_obsazenych[k, 0] > x_min and souradnice_obsazenych[k, 1] < y_max and souradnice_obsazenych[k, 1] > y_min:
                    napojene.append(pozice_obsazene[k])
            j = j+1
        if vyherni_kontrola_trojice(napojene) == True:
            vyhra = True
    return  vyhra

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if stav == 2:
                    stav = 3
                elif stav == 4:
                    stav = 5
            elif event.key == pygame.K_BACKSPACE:
                odpoved = odpoved[:-1]
            else:
                odpoved += event.unicode

    if stav == 1:
        podminka_trojice, nejkratsi = kontrola_trojice('red')
        if podminka_trojice == True:
            vyhra = podminka_spojeni(nejkratsi, 'red')
            if vyhra == True:
                stav = 6
        podminka_trojice, nejkratsi = kontrola_trojice('green')
        if podminka_trojice == True:
            vyhra = podminka_spojeni(nejkratsi, 'green')
            if vyhra == True:
                stav = 6
        vypis_desky(poradi_hrac)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_pos = pygame.mouse.get_pos()
                vybrane_pole = uvnitr_sestiuhelniku(click_pos, pozice)
                if vybrane_pole != None:
                    if barvy[vybrane_pole] == 'white':
                        stav=2
                    elif barvy[vybrane_pole] == 'black':
                        stav=4
    elif stav == 2:
        screen.fill("blue")
        text_surface = font.render(str(seznam_otazek[vybrane_pole]), True, 'black')
        screen.blit(text_surface, (width/2, height/2-100))
        text_surface = font.render("Tvoje odpoved: " + odpoved, True, 'black')
        screen.blit(text_surface, (width/2-100, height/2+100))
    elif stav == 3:
        if str(odpoved) == str(seznam_odpovedi[vybrane_pole]) and poradi_hrac == 'hraje červená':
            barvy[vybrane_pole] = 'red'
            vybrane_pole = 0
            poradi_hrac = 'hraje zelená'
            odpoved = ''
            stav = 1
        elif str(odpoved) == str(seznam_odpovedi[vybrane_pole]) and poradi_hrac == 'hraje zelená':
            barvy[vybrane_pole] = 'green'
            vybrane_pole = 0
            poradi_hrac = 'hraje červená'
            odpoved = ''
            stav = 1
        elif str(odpoved) != str(seznam_odpovedi[vybrane_pole]) and poradi_hrac == 'hraje červená':
            barvy[vybrane_pole] = 'black'
            poradi_hrac = 'hraje zelená'
            vybrane_pole = 0
            odpoved = ''
            stav = 1
        elif str(odpoved) != str(seznam_odpovedi[vybrane_pole]) and poradi_hrac == 'hraje zelená':
            barvy[vybrane_pole] = 'black'
            poradi_hrac = 'hraje červená'
            vybrane_pole = 0
            odpoved = ''
            stav = 1
    elif stav == 4:
        screen.fill("blue")
        text_surface = font.render(str(seznam_otazek_cerne[poradi_cerne]), True, 'black')
        screen.blit(text_surface, (width/2, height/2-100))
        text_surface = font.render("Tvoje odpoved: " + odpoved, True, 'black')
        screen.blit(text_surface, (width/2-100, height/2+100))
    elif stav == 5:
        if str(odpoved) == str(seznam_odpovedi_cerne[poradi_cerne]) and poradi_hrac == 'hraje červená':
            barvy[vybrane_pole] = 'red'
            poradi_cerne = poradi_cerne+1
            vybrane_pole = 0
            poradi_hrac = 'hraje zelená'
            odpoved = ''
            stav = 1
        elif str(odpoved) == str(seznam_odpovedi_cerne[poradi_cerne]) and poradi_hrac == 'hraje zelená':
            barvy[vybrane_pole] = 'green'
            poradi_cerne = poradi_cerne+1
            vybrane_pole = 0
            poradi_hrac = 'hraje červená'
            odpoved = ''
            stav = 1
        elif str(odpoved) != str(seznam_odpovedi_cerne[poradi_cerne]) and poradi_hrac == 'hraje červená':
            barvy[vybrane_pole] = 'black'
            poradi_hrac = 'hraje zelená'
            poradi_cerne = poradi_cerne+1
            vybrane_pole = 0
            odpoved = ''
            stav = 1
        elif str(odpoved) != str(seznam_odpovedi_cerne[poradi_cerne]) and poradi_hrac == 'hraje zelená':
            barvy[vybrane_pole] = 'black'
            poradi_hrac = 'hraje červená'
            poradi_cerne = poradi_cerne+1
            vybrane_pole = 0
            odpoved = ''
            stav = 1
    elif stav == 6:
        screen.fill("blue")
        if poradi_hrac == 'hraje červená':
            text_surface = font.render('vyhrává zelený', True, 'black')
            screen.blit(text_surface, (width / 2-100, height / 2))
        elif poradi_hrac == 'hraje zelená':
            text_surface = font.render('vyhrává červený', True, 'black')
            screen.blit(text_surface, (width / 2-100, height / 2))
    pygame.display.flip()
    clock.tick(30)
pygame.quit()