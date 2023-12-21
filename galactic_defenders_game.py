import pygame
import random
pygame.init()
#fonction pour afficher un texte à un endroit précis
def texte(x, y, taille_texte, texte, couleur):
    font = pygame.font.Font(None, taille_texte)
    text = font.render(texte, True, couleur)
    screen.blit(text,( x, y))

#gérer les mouvements du vaisseau
def mouvement_vaisseau():
    global  pos_vaisseau_x, pos_vaisseau_y
    touches_clavier_appuyées = pygame.key.get_pressed()
    if touches_clavier_appuyées[pygame.K_q] and pos_vaisseau_x - vitesse_vaisseau > 0: # si on appuie sur "q"
        pos_vaisseau_x -= vitesse_vaisseau
    if touches_clavier_appuyées[pygame.K_d] and pos_vaisseau_x + longueur_vaisseau_x + vitesse_vaisseau < screen_width: # si on appuie sur "d"
        pos_vaisseau_x += vitesse_vaisseau
    screen.blit(vaisseau, (pos_vaisseau_x ,pos_vaisseau_y )) # afficher le vaisseau

def collision_ennemis( longueur_ennemis_y, longueur_ennemis_x, pos_vaisseau_y, pos_vaisseau_x, longueur_vaisseau_x, nbre_ennemis):
    global barre_verte_longueur_x, ennemis_y, ennemis_x
    for i in range(nbre_ennemis): 
        if ennemis_y[i] + longueur_ennemis_y >= pos_vaisseau_y and not (ennemis_x[i] + longueur_ennemis_x < pos_vaisseau_x or ennemis_x[i] > pos_vaisseau_x + longueur_vaisseau_x):
            ennemis_x[i] = random.randint(0, screen_width - longueur_ennemis_x)
            ennemis_y[i] = 0
            barre_verte_longueur_x -= 4
        elif ennemis_y[i] > screen_height + 120:
            ennemis_x[i] = random.randint(0, screen_width - longueur_ennemis_x)
            ennemis_y[i] = 0
            barre_verte_longueur_x -= 4

# barre de vie du vaisseau
def barre_vie_vaisseau(pos_vaisseau_x, pos_vaisseau_y, longueur_vaisseau_y, barre_rouge_longueur_x, barre_rouge_longueur_y, barre_verte_longueur_y):
    global barre_verte_longueur_x, game_over, jeu
    pos_barre_rouge_x = pos_barre_verte_x = pos_vaisseau_x
    pos_barre_rouge_y = pos_barre_verte_y = pos_vaisseau_y + longueur_vaisseau_y
    pygame.draw.rect(screen, rouge, [pos_barre_rouge_x, pos_barre_rouge_y, barre_rouge_longueur_x, barre_rouge_longueur_y])
    pygame.draw.rect(screen, vert, [pos_barre_verte_x, pos_barre_verte_y, barre_verte_longueur_x, barre_verte_longueur_y])
    if barre_verte_longueur_x <= 0:
        game_over = True
        jeu = False

def réinitialiser():
    global barre_verte_longueur_x, ennemis_x, ennemis_y, score_nb
    score_nb = 0
    barre_verte_longueur_x = longueur_vaisseau_x
    for i in range(nbre_ennemis):
        ennemis_x[i] = random.randint(0, screen_width - longueur_ennemis_x)
        ennemis_y[i] = 0

def tirs(longueur_tir_x, longueur_tir_y, vitesse_tir, pos_vaisseau_x, pos_vaisseau_y):
    global tir_x, tir_y
    clic_souris = pygame.mouse.get_pressed()
    if clic_souris[0]:
        tir_x = pos_vaisseau_x + longueur_vaisseau_x//2 - longueur_tir_x//2
        tir_y = pos_vaisseau_y -  longueur_tir_x
    tir_y -= vitesse_tir
    pygame.draw.rect(screen, rouge, [tir_x , tir_y, longueur_tir_x, longueur_tir_y])

def collision_tirs(longueur_ennemis_y, longueur_ennemis_x, nbre_ennemis, longueur_tir_x, longueur_tir_y):
    global tir_x, tir_y, ennemis_y, ennemis_x, score_nb
    for ennemis in range(nbre_ennemis):
        x_collision = True if not(ennemis_x[ennemis] + longueur_ennemis_x < tir_x or ennemis_x[ennemis] > tir_x + longueur_tir_x) else False
        y_collision = True if not(ennemis_y[ennemis] + longueur_ennemis_y < tir_y or ennemis_y[ennemis] > tir_y + longueur_tir_y) else False
        if x_collision and y_collision:
            ennemis_x[ennemis] = random.randint(0, screen_width - longueur_ennemis_x)
            ennemis_y[ennemis] = 0
            tir_x = 2000
            tir_y = 2000
            score_nb += 1

def score_affichage(score_nb):
    global win, jeu
    texte(0, 0, 25, "Score :" + str(score_nb), blanc)
    if score_nb >= 50:
        win = True
        jeu = False


# Couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
gris_clair = (170, 170, 170)
gris_foncé = (100, 100, 100)
rouge = (255, 0, 0)
vert = (0, 255, 0)

# Dimensions de la fenêtre
screen_width = 800
screen_height = 600

# Booléen servants à déterminer quelle fenêtre afficher
running = True
menu_démarrage = True
jeu = False
game_over = False
win = False

# Image utilisée en fond
image_de_fond = pygame.image.load("image_de_fond.jpg")
image_de_fond = pygame.transform.scale(image_de_fond,(screen_width, screen_height)) # modifier la taille de l'image

# Créer la fenêtre
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Galactic Defenders")

# bouton démarrer
longueur_bouton_démarrer_x = 120
longueur_bouton_démarrer_y = 60
pos_bouton_démarrer_x = screen_width//2 - longueur_bouton_démarrer_x//2
pos_bouton_démarrer_y = screen_height//2 - longueur_bouton_démarrer_y//2
surface_bouton_démarrer = [pos_bouton_démarrer_x , pos_bouton_démarrer_y, longueur_bouton_démarrer_x, longueur_bouton_démarrer_y]
taille_texte_bouton_démarrer = 29

# Titre "Galactic Defenders" en haut au centre de la fenêtre
taille_titre = 50
pos_titre_x = 240
pos_titre_y = 100

# Vaisseau du joueur
longueur_vaisseau_x = 40
longueur_vaisseau_y = 52
vaisseau = pygame.image.load("ship.png")
vaisseau = pygame.transform.scale(vaisseau,( longueur_vaisseau_x, longueur_vaisseau_y)) # redimensionner la taille x et y de l'image du vaisseau
pos_vaisseau_x = screen_width//2 - longueur_vaisseau_x//2
pos_vaisseau_y = screen_height - longueur_bouton_démarrer_y
vitesse_vaisseau = 6
barre_rouge_longueur_x = barre_verte_longueur_x = longueur_vaisseau_x # barre de vie
barre_rouge_longueur_y = barre_verte_longueur_y = 10

# définir la vitesse du jeu
FPS = 60
clock = pygame.time.Clock()

# ennemis
longueur_ennemis_x = 40
longueur_ennemis_y = 40
ennemis = pygame.image.load("ennemis.png")
ennemis = pygame.transform.scale(ennemis, (longueur_ennemis_x ,longueur_ennemis_y ))
vitesse_ennemis = 3
nbre_ennemis = 2
ennemis_x = []
ennemis_y = []
for i in range(nbre_ennemis):
    ennemis_x.append(random.randint(0, screen_width - longueur_ennemis_x))
    ennemis_y.append(0)

# tirs du vaisseau
longueur_tir_x = 5
longueur_tir_y = 10
vitesse_tir = 7
tir_x = 2000
tir_y = 2000

#score
score_nb = 0

while running:
    clock.tick(FPS)
    pygame.display.flip()# Cela sert à mettre à jour l'affichage de l'écran
    mouse = pygame.mouse.get_pos()# Ici on récupère la position x et y du curseur de la souris par rapport à la fenêtre
    screen.blit(image_de_fond,(0 ,0)) # afficher l'image de fond

    # Récupérer les événements (exemple: clics de la souris...)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # condition servant à fermer le jeu si l'utilisateur clique sur la croix en haut à droite
            running = False

    # Condition pour afficher ou non le menu démarrage
    if menu_démarrage:
        # conditions pour passer à la fenêtre de jeu: clic de la souris et les coordonnées du curseur sur le bouton Démarrer
        if event.type == pygame.MOUSEBUTTONDOWN and pos_bouton_démarrer_x <= mouse[0] <= pos_bouton_démarrer_x + longueur_bouton_démarrer_x and pos_bouton_démarrer_y <= mouse[1] <= pos_bouton_démarrer_y + longueur_bouton_démarrer_y:
            menu_démarrage = False
            jeu = True
        texte(pos_titre_x, pos_titre_y, taille_titre, "Galactic Defenders", blanc) # afficher le texte "Galactic Defenders" dans la fenêtre, au-dessus du bouton Démarrer grâce à une fonction définie
        # Conditions if...else servant à modifier la couleur du rectangle (la couleur de fond du bouton Démarrer) suivant si le curseur est ou non sur le bouton
        if pos_bouton_démarrer_x <= mouse[0] <= pos_bouton_démarrer_x + longueur_bouton_démarrer_x and pos_bouton_démarrer_y <= mouse[1] <= pos_bouton_démarrer_y + longueur_bouton_démarrer_y:
            pygame.draw.rect(screen, gris_clair, surface_bouton_démarrer)
        else:
            pygame.draw.rect(screen, gris_foncé, surface_bouton_démarrer)
        # Ici on affiche par dessus le rectangle le texte "Démarrer" à l'aide de la fonction texte() définie au-début
        texte(pos_bouton_démarrer_x + 15, pos_bouton_démarrer_y + 18, taille_texte_bouton_démarrer, "Démarrer", blanc)

    # Condition pour afficher ou non la page de jeu
    if jeu:
        mouvement_vaisseau()
        for i in range(nbre_ennemis):
            ennemis_y[i] += vitesse_ennemis
            screen.blit(ennemis, (ennemis_x[i] ,ennemis_y[i]))
        barre_vie_vaisseau(pos_vaisseau_x, pos_vaisseau_y, longueur_vaisseau_y, barre_rouge_longueur_x, barre_rouge_longueur_y, barre_verte_longueur_y)
        collision_ennemis( longueur_ennemis_y, longueur_ennemis_x, pos_vaisseau_y, pos_vaisseau_x, longueur_vaisseau_x, nbre_ennemis)
        tirs(longueur_tir_x, longueur_tir_y, vitesse_tir, pos_vaisseau_x, pos_vaisseau_y)
        collision_tirs(longueur_ennemis_y, longueur_ennemis_x, nbre_ennemis, longueur_tir_x, longueur_tir_y)
        score_affichage(score_nb)

    if game_over:
        texte(pos_titre_x + 60, pos_titre_y, taille_titre, "Game Over", blanc)
        if pos_bouton_démarrer_x <= mouse[0] <= pos_bouton_démarrer_x + longueur_bouton_démarrer_x and pos_bouton_démarrer_y <= mouse[1] <= pos_bouton_démarrer_y + longueur_bouton_démarrer_y:
            pygame.draw.rect(screen, gris_clair, surface_bouton_démarrer)
        else:
            pygame.draw.rect(screen, gris_foncé, surface_bouton_démarrer)
        texte(pos_bouton_démarrer_x + 30, pos_bouton_démarrer_y + 18, taille_texte_bouton_démarrer, "Retour", blanc)
        if event.type == pygame.MOUSEBUTTONDOWN and pos_bouton_démarrer_x <= mouse[0] <= pos_bouton_démarrer_x + longueur_bouton_démarrer_x and pos_bouton_démarrer_y <= mouse[1] <= pos_bouton_démarrer_y + longueur_bouton_démarrer_y:
            menu_démarrage = True
            game_over = False
            pygame.time.wait(150)
            réinitialiser()
    if win:
        texte(pos_titre_x + 15, pos_titre_y, taille_titre, "Vous avez gagné!", blanc)
        if pos_bouton_démarrer_x <= mouse[0] <= pos_bouton_démarrer_x + longueur_bouton_démarrer_x and pos_bouton_démarrer_y <= mouse[1] <= pos_bouton_démarrer_y + longueur_bouton_démarrer_y:
            pygame.draw.rect(screen, gris_clair, surface_bouton_démarrer)
        else:
            pygame.draw.rect(screen, gris_foncé, surface_bouton_démarrer)
        texte(pos_bouton_démarrer_x + 30, pos_bouton_démarrer_y + 18, taille_texte_bouton_démarrer, "Retour", blanc)
        if event.type == pygame.MOUSEBUTTONDOWN and pos_bouton_démarrer_x <= mouse[0] <= pos_bouton_démarrer_x + longueur_bouton_démarrer_x and pos_bouton_démarrer_y <= mouse[1] <= pos_bouton_démarrer_y + longueur_bouton_démarrer_y:
            menu_démarrage = True
            win = False
            pygame.time.wait(150)
            réinitialiser()
        
pygame.quit()