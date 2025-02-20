import pygame
import random
import json
import os

# Chargement des données Pokémon
with open("pokemon_data.json", "r") as file:
    pokemon_data = json.load(file)

# Chemin du dossier des images
image_path = "image"

# Liste des starters et leurs évolutions
starters = {
    "chespin": "quilladin",
    "fennekin": "braixen",
    "froakie": "frogadier",
    "rowlet": "dartrix"
}

final_evolutions = {
    "quilladin": "chesnaught",
    "braixen": "delphox",
    "frogadier": "greninja",
    "dartrix": "decidueye"
}

def charger_image(nom):
    chemin = os.path.join(image_path, f"{nom}.png")
    if os.path.exists(chemin):
        return pygame.image.load(chemin)
    return None

# Sélectionner un Pokémon
def choisir_pokemon(nom=None):
    if not nom:
        nom, data = random.choice(list(pokemon_data.items()))
    else:
        data = pokemon_data[nom]
    types = data["TYPE"]
    attaques = random.sample(data["ATTACK list"], min(len(types), 2))
    image = charger_image(nom)
    return {
        "nom": nom,
        "pv": data["PV"],
        "pv_max": data["PV"],
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

# Chargement de l'image de fond
background = pygame.image.load("ring.png")

# Choisir le premier Pokémon du joueur
equipe_joueur = [choisir_pokemon(random.choice(list(starters.keys())))]

# Sélection du premier Pokémon adverse
adversaire = choisir_pokemon()

# Initialisation du niveau
level = 1

# Boucle principale
running = True
joueur_actuel = equipe_joueur[0]

def attaque_adversaire():
    attaque = random.choice(adversaire["attaques"])
    degats = random.randint(10 + level, 20 + level)
    joueur_actuel["pv"] -= degats
    print(f"{adversaire['nom']} utilise {attaque} et inflige {degats} dégâts!")
    if joueur_actuel["pv"] <= 0:
        print(f"{joueur_actuel['nom']} a été vaincu!")
        return True
    return False

while running:
    ecran.blit(background, (0, 0))
    
    # Gestion de l'évolution du Pokémon
    if level == 6 and joueur_actuel["nom"] in starters:
        joueur_actuel = choisir_pokemon(starters[joueur_actuel["nom"]])
        equipe_joueur[0] = joueur_actuel
        print(f"{joueur_actuel['nom']} a évolué !")
    elif level == 16 and joueur_actuel["nom"] in final_evolutions:
        joueur_actuel = choisir_pokemon(final_evolutions[joueur_actuel["nom"]])
        equipe_joueur[0] = joueur_actuel
        print(f"{joueur_actuel['nom']} a atteint sa forme finale !")
    
    # Affichage des Pokémon (images)
    if joueur_actuel["image"]:
        ecran.blit(joueur_actuel["image"], (100, 200))
    if adversaire["image"]:
        ecran.blit(adversaire["image"], (600, 200))
    
    # Affichage des PV et du niveau
    joueur_pv_text = defaut_font.render(f"{joueur_actuel['nom']}: {joueur_actuel['pv']} PV", True, noir)
    adversaire_pv_text = defaut_font.render(f"{adversaire['nom']}: {adversaire['pv']} PV", True, noir)
    level_text = defaut_font.render(f"Niveau: {level}", True, noir)
    ecran.blit(joueur_pv_text, (50, 50))
    ecran.blit(adversaire_pv_text, (550, 50))
    ecran.blit(level_text, (350, 20))
    
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
                    degats = random.randint(10 + level, 20 + level)
                    adversaire["pv"] -= degats
                    print(f"{joueur_actuel['nom']} utilise {attaque} et inflige {degats} dégâts!")
                    if adversaire["pv"] <= 0:
                        level += 1  # Incrémentation du niveau
                        joueur_actuel["pv"] = joueur_actuel["pv_max"]  # Restauration des PV
                        adversaire = choisir_pokemon()  # Nouveau combat contre un Pokémon aléatoire
                    else:
                        if attaque_adversaire():
                            running = False
                    break

pygame.quit()
