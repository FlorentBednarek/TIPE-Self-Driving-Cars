import pygame

# Maniabilité du véhicule (nombre de degrés par fps dans un virage)
car_maniability = 2.5

# Touches de contrôle de la voiture, gauche et droite
left_key = pygame.K_LEFT
right_key = pygame.K_RIGHT

# Contrôle manuel de la voiture
manual_control = True

# Nombre de voitures lors du mode automatique
cars_number = 1

# Images par seconde
fps = 60

# Couleur de la voiture (mode manuel uniquement)
car_color = "#FF0000"

# Taille de la fenêtre
try :
	screen_size = [1200,700]
except :
	screen_size = [1200,700]
