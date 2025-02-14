import pygame
import random
import json
import os

# Chargement des données Pokémon
with open("pokemon_data.json", "r") as file:
    pokemon_data = json.load(file)

# Chemin du dossier des images
image_path = "Image"

def charger_image(nom):
    chemin = os.path.join(image_path, f"{nom}.png")
    if os.path.exists(chemin):
        return pygame.image.load(chemin)
    return None

# Sélectionner un Pokémon au hasard
def choisir_pokemon():
    nom, data = random.choice(list(pokemon_data.items()))
    types = data["TYPE"]
    attaques = random.sample(data["ATTACK list"], min(len(types), 2))
    image = charger_image(nom)
    return {
        "nom": nom,
        "pv": data["PV"],
        "vitesse": data["VITESSE"],
        "attaques": attaques,
        "image": image
    }

# Initialisation de Pygame
pygame.init()

# Constantes
taille_ecran = (800, 600)
blanc = (255, 255, 255)
noir = (0, 0, 0)
bleu = (0, 0, 255)

ecran = pygame.display.set_mode(taille_ecran)
pygame.display.set_caption("Combat Pokémon")

defaut_font = pygame.font.Font(None, 36)

# Choisir deux Pokémon
pokemon1 = choisir_pokemon()
pokemon2 = choisir_pokemon()

# Boucle principale
running = True
joueur_actuel = pokemon1
adversaire = pokemon2

while running:
    ecran.fill(blanc)
    
    # Affichage des Pokémon (images)
    if pokemon1["image"]:
        ecran.blit(pokemon1["image"], (100, 200))
    if pokemon2["image"]:
        ecran.blit(pokemon2["image"], (600, 200))
    
    # Affichage des PV
    pokemon1_pv_text = defaut_font.render(f"{pokemon1['nom']}: {pokemon1['pv']} PV", True, noir)
    pokemon2_pv_text = defaut_font.render(f"{pokemon2['nom']}: {pokemon2['pv']} PV", True, noir)
    ecran.blit(pokemon1_pv_text, (50, 50))
    ecran.blit(pokemon2_pv_text, (550, 50))
    
    # Affichage des boutons d'attaque
    boutons = []
    y_offset = 400
    for i, attaque in enumerate(joueur_actuel["attaques"]):
        bouton = pygame.Rect(50, y_offset + i * 50, 200, 40)
        pygame.draw.rect(ecran, bleu, bouton)
        texte = defaut_font.render(attaque, True, blanc)
        ecran.blit(texte, (60, y_offset + i * 50 + 10))
        boutons.append((bouton, attaque))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for bouton, attaque in boutons:
                if bouton.collidepoint(event.pos):
                    degats = random.randint(10, 20)
                    adversaire["pv"] -= degats
                    if adversaire["pv"] < 0:
                        adversaire["pv"] = 0
                    print(f"{joueur_actuel['nom']} utilise {attaque} et inflige {degats} dégâts!")
                    joueur_actuel, adversaire = adversaire, joueur_actuel  # Changement de tour
    
    if pokemon1["pv"] == 0 or pokemon2["pv"] == 0:
        print("Combat terminé !")
        running = False
    
pygame.quit()
