import pygame

# Maniabilité du véhicule (nombre de degrés max par frame dans un virage)
car_maniability = 1.5

# Touches de contrôle de la voiture, gauche et droite
left_key = pygame.K_LEFT
right_key = pygame.K_RIGHT

# Contrôle manuel de la voiture (True/False)
manual_control = False

# Affichage du raycasting (None/'Ray'/'Cross')
display_rays = None

# Nombre de voitures lors du mode automatique
cars_number = 30

# Images par seconde
fps = 20

# Couleur de la voiture (mode manuel uniquement)
car_color = "#FF0000"

# Taille de la fenêtre
screen_size = [1200,700]
