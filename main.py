import pygame
import sys
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def initialiser_pygame():
    """
    Initialise Pygame.

    :return: None
    """
    pygame.init()

def charger_musique(chemin, volume):
    """
    Charge et joue une musique en boucle.

    :param chemin: (str) Chemin vers le fichier de musique.
    :param volume: (float) Volume de la musique (entre 0 et 1).
    :return: None

    >>> charger_musique('zelda.mp3', 0.1)
    """
    if os.path.exists(chemin):
        pygame.mixer.music.load(chemin)
        pygame.mixer.music.play(-1)  # Jouer en boucle
        pygame.mixer.music.set_volume(volume)  # Baisser le volume
    else:
        print(f"Avertissement : fichier musique non trouvé : {chemin}")

def empecher_sortie_ecran(s, largeur, hauteur, taille_grille):
    """
    Empêche un personnage de sortir de l'écran en ajustant ses coordonnées x et y.

    :param s: (dict) Un dictionnaire représentant un personnage, avec des clés 'x' et 'y'.
    :param largeur: (int) La largeur de l'écran.
    :param hauteur: (int) La hauteur de l'écran.
    :param taille_grille: (int) La taille de la grille de jeu.
    :return: None

    >>> s = {'x': 900, 'y': 900}
    >>> empecher_sortie_ecran(s, 800, 800, 40)
    >>> print(s)
    {'x': 760, 'y': 760}
    """
    s['x'] = max(0, min(s['x'], largeur - taille_grille))
    s['y'] = max(0, min(s['y'], hauteur - taille_grille))

def reproduction(liste_personnages, max_personnages, taille_grille, largeur, hauteur, prob_reproduction):
    """
    Gère la reproduction des personnages dans le jeu.

    :param liste_personnages: (list) Liste des personnages.
    :param max_personnages: (int) Nombre maximum de personnages.
    :param taille_grille: (int) Taille de la grille de jeu.
    :param largeur: (int) Largeur de la fenêtre de jeu.
    :param hauteur: (int) Hauteur de la fenêtre de jeu.
    :param prob_reproduction: (float) Probabilité de reproduction.
    :return: None

    >>> liste_personnages = [(0, 0), (40, 40)]
    >>> reproduction(liste_personnages, 4, 40, 800, 800, 0.5)
    >>> len(liste_personnages) >= 2
    True
    """
    if len(liste_personnages) < max_personnages:
        for i in range(len(liste_personnages)):
            for j in range(i+1, len(liste_personnages)):
                if abs(liste_personnages[i][0] - liste_personnages[j][0]) <= taille_grille and abs(liste_personnages[i][1] - liste_personnages[j][1]) <= taille_grille:
                    prob = random.random()
                    if prob < prob_reproduction:
                        liste_personnages.append((random.randint(0, largeur), random.randint(0, hauteur)))


def dessiner_personnages(fenetre, personnage, liste_personnages):
    """
    Dessine les personnages sur la fenêtre de jeu.

    :param fenetre: (pygame.Surface) La fenêtre de jeu.
    :param personnage: (pygame.Surface) L'image du personnage.
    :param liste_personnages: (list) Liste des personnages.
    :return: None
    """
    for x, y in liste_personnages:
        fenetre.blit(personnage, (x, y))

# Initialisation de Pygame
initialiser_pygame()

# Charger la musique
music_path = os.path.join(BASE_DIR, 'zelda.mp3')
charger_musique(music_path, 0.1)

# Définir la taille de la fenêtre
largeur, hauteur = 800, 800
taille_fenetre = (largeur, hauteur)

# Créer la fenêtre
fenetre = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Zombie Life")

# Charger l'image de fond
bg_path = os.path.join(BASE_DIR, 'bg.png')
fond = pygame.image.load(bg_path)

# Redimensionner l'image de fond
fond = pygame.transform.scale(fond, (largeur, hauteur))

# Position initiale des sprites
x_schwarze, y_schwarze = random.randint(0, largeur), random.randint(0, hauteur)
x_zombie, y_zombie = random.randint(0, largeur), random.randint(0, hauteur)
x_link, y_link = random.randint(0, largeur), random.randint(0, hauteur)

# Sprites
stallone_path = os.path.join(BASE_DIR, 'stallone.png')
schwarze = pygame.image.load(stallone_path)

zombie_path = os.path.join(BASE_DIR, 'zombie.png')
zombie = pygame.image.load(zombie_path)

link_path = os.path.join(BASE_DIR, 'link.png')
link = pygame.image.load(link_path)

# Redimensionner sprites
schwarze = pygame.transform.scale(schwarze, (40, 40))
zombie = pygame.transform.scale(zombie, (40, 40))
link = pygame.transform.scale(link, (40, 40))

# Charger la police
font_path = os.path.join(BASE_DIR, 'RetroGaming.ttf')
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 24)
else:
    print(f"Avertissement : police non trouvée : {font_path}")
    font = pygame.font.Font(None, 24)  # Police par défaut

# Taille de la grille
taille_grille = 60

# Vitesse des personnages
vitesse_schwarze = 0.6
vitesse_zombie = 0.2
vitesse_link = 0.4

# Nombre de zombies et de links
nombre_zombies = 50
nombre_links = 40

# Liste des zombies et des links
liste_zombies = [(random.randint(0, largeur), random.randint(0, hauteur)) for _ in range(nombre_zombies)]
liste_links = [(random.randint(0, largeur), random.randint(0, hauteur)) for _ in range(nombre_links)]
liste_schwarze = []  # Liste initiale des schwarze vide

temps_dernier_link = 0  # Temps depuis le dernier link ajouté
temps_dernier_schwarze = 0  # Temps depuis le dernier schwarze ajouté
temps_derniere_augmentation = 0  # Temps depuis la dernière augmentation de taille
taille_schwarze = 50  # Taille initiale de schwarze

temps_derniere_acceleration = 0  # Temps depuis la dernière accélération
vitesse_jeu = 30  # Vitesse initiale du jeu en images par seconde

max_links = 30  # Limite maximale de links
max_zombies = 40  # Limite maximale de zombies

prob_reproduction = 0.25  # Probabilité de reproduction

# Ajouter 1 schwarze au démarrage
for _ in range(1):
    x_schwarze, y_schwarze = random.randint(0, largeur), random.randint(0, hauteur)
    liste_schwarze.append({'x': x_schwarze, 'y': y_schwarze, 'vitesse': 1, 'taille': 40})

# Boucle de jeu
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessiner l'image de fond
    fenetre.blit(fond, (0, 0))

    temps_actuel = pygame.time.get_ticks()  # Temps actuel en millisecondes


    # Augmenter la taille de schwarze toutes les secondes
    if temps_actuel - temps_derniere_augmentation >= 2000:  
        for s in liste_schwarze:
            s['taille'] += 30  # Augmenter la taille de schwarze
        temps_derniere_augmentation = temps_actuel


    # Accélérer le jeu toutes les 2 secondes
    if temps_actuel - temps_derniere_acceleration >= 2000:  # 2000 mllisecondes = 2 secondes
        vitesse_jeu += 10
        temps_derniere_acceleration = temps_actuel


    # Ajouter un nouveau link toutes les secondes
    if temps_actuel - temps_dernier_link >= 1000 and len(liste_links) < max_links:  # 3000 millisecondes = 3 secondes
        liste_links.append((random.randint(0, largeur), random.randint(0, hauteur)))
        temps_dernier_link = temps_actuel


    # Ajouter 1 schwarze après 5 secondes
    if temps_actuel - temps_dernier_schwarze >= 5000:  # 5 secondes au lieu de 60
        for _ in range(1):
            x_schwarze, y_schwarze = random.randint(0, largeur), random.randint(0, hauteur)
            liste_schwarze.append({'x': x_schwarze, 'y': y_schwarze, 'vitesse': 1, 'taille': 40})
        temps_dernier_schwarze = temps_actuel

    # Déplacer les schwarze
    for s in liste_schwarze:
        s['x'] = (s['x'] + random.uniform(-s['vitesse'], s['vitesse']) * taille_grille)
        s['y'] = (s['y'] + random.uniform(-s['vitesse'], s['vitesse']) * taille_grille)
        empecher_sortie_ecran(s, largeur, hauteur, taille_grille)
    
    # Schwarze tue les zombies
    for s in liste_schwarze:
        liste_zombies = [z for z in liste_zombies if abs(z[0] - s['x']) > s['taille'] or abs(z[1] - s['y']) > s['taille']]


    # Vérifier si la liste des zombies est vide
    if not liste_zombies:
        # Créer un texte
        text = font.render("Félicitations !! vous avez tué tous les zombies !", True, (0, 0, 0))
       
        # Obtenir le rectangle du texte
        text_rect = text.get_rect()

        # Centrer le rectangle
        text_rect.center = (largeur // 2, hauteur // 2)

        # Dessiner un cadre blanc autour du texte
        pygame.draw.rect(fenetre, (255, 255, 255), text_rect.inflate(20, 20))

        # Dessiner le texte
        fenetre.blit(text, text_rect)

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Attendre 5 secondes
        pygame.time.wait(5000)

        pygame.quit()
        sys.exit()


    # Logique du jeu
    x_schwarze = (x_schwarze + random.uniform(-vitesse_schwarze, vitesse_schwarze) * taille_grille)
    y_schwarze = (y_schwarze + random.uniform(-vitesse_schwarze, vitesse_schwarze) * taille_grille)

    # Empêcher schwarze de sortir de l'écran
    x_schwarze = max(0, min(x_schwarze, largeur - taille_grille))
    y_schwarze = max(0, min(y_schwarze, hauteur - taille_grille))

    # Mouvement des zombies et des links
    for i in range(len(liste_zombies)):
        x, y = liste_zombies[i]
        x = (x + random.uniform(-vitesse_zombie, vitesse_zombie) * taille_grille)
        y = (y + random.uniform(-vitesse_zombie, vitesse_zombie) * taille_grille)

        # Empêcher les zombies de sortir de l'écran
        x = max(0, min(x, largeur - taille_grille))
        y = max(0, min(y, hauteur - taille_grille))

        liste_zombies[i] = (x, y)

    for i in range(len(liste_links)):
        x, y = liste_links[i]
        x = (x + random.uniform(-vitesse_link, vitesse_link) * taille_grille)
        y = (y + random.uniform(-vitesse_link, vitesse_link) * taille_grille)

        # Empêcher les links de sortir de l'écran
        x = max(0, min(x, largeur - taille_grille))
        y = max(0, min(y, hauteur - taille_grille))

        liste_links[i] = (x, y)



    # Schwarze tue les zombies proches
    liste_zombies = [z for z in liste_zombies if abs(z[0] - x_schwarze) > taille_grille or abs(z[1] - y_schwarze) > taille_grille]

    # Les links et les zombies se tuent mutuellement lorsqu'ils sont proches, liste_links[:] et liste_zombies[:] sont utilisés pour créer des copies des listes, car les modifier crée des problèmes
    for l in liste_links[:]:
        for z in liste_zombies[:]:
            if abs(l[0] - z[0]) <= taille_grille and abs(l[1] - z[1]) <= taille_grille:
                # Générer un nombre aléatoire entre 0 et 1
                prob = random.random()
                # Si le nombre est inférieur à 0.3, le link meurt
                if prob < 0.5:
                    if l in liste_links:  # Vérifier si le link est dans la liste avant de le supprimer
                        liste_links.remove(l)
                # Sinon, le zombie meurt
                else:
                    if z in liste_zombies:  # Vérifier si le zombie est dans la liste avant de le supprimer
                        liste_zombies.remove(z)


    # Les links se reproduisent
    reproduction(liste_links, max_links, taille_grille, largeur, hauteur, prob_reproduction)

    # Les zombies se reproduisent
    reproduction(liste_zombies, max_zombies, taille_grille, largeur, hauteur, prob_reproduction)

    """# Dessiner la grille
    for x in range(0, largeur, taille_grille):
        pygame.draw.line(fenetre, (0, 0, 0), (x, 0), (x, hauteur))
    for y in range(0, hauteur, taille_grille):
        pygame.draw.line(fenetre, (0, 0, 0), (0, y), (largeur, y))"""


    # Dessiner les personnages
    dessiner_personnages(fenetre, schwarze, [(x_schwarze, y_schwarze)])
    dessiner_personnages(fenetre, zombie, liste_zombies)
    dessiner_personnages(fenetre, link, liste_links)

    # Dessiner les schwarze supplémentaires
    for s in liste_schwarze:
        schwarze_redimensionne = pygame.transform.scale(schwarze, (s['taille'], s['taille']))  # Redimensionner schwarze
        fenetre.blit(schwarze_redimensionne, (s['x'], s['y']))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôle de la fréquence d'images
    clock.tick(vitesse_jeu)


if __name__ == "__main__":
    import doctest
    doctest.testmod()