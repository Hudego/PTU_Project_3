"""
python version: 3.8.20
"""


import os
from pymol import cmd

def obtenir_fragments_depuis_dossier(dossier):
    
    """
    Récupère tous les fichiers .pdb d'un dossier donné, en excluant les fichiers correspondant aux protéines entières.
    """
    fragments = []
    for fichier in os.listdir(dossier):
        if fichier.endswith('.pdb') and 'fragment' in fichier:  
            fragments.append(os.path.join(dossier, fichier))
    return fragments

def nettoyer_dossier(dossier):

    """
    Supprime tous les fichiers dans le dossier spécifié.
    """

    if os.path.exists(dossier):
        for fichier in os.listdir(dossier):
            chemin_fichier = os.path.join(dossier, fichier)
            if os.path.isfile(chemin_fichier):
                os.remove(chemin_fichier)
        print(f"Tous les fichiers dans le dossier '{dossier}' ont été supprimés.")
    else:
        os.makedirs(dossier)  
        print(f"Le dossier '{dossier}' a été créé.")


def superposer_et_enregistrer_image(modele, dossier_fragments, output_dir, longueur_aa_min=40):

    # Nettoye le dossier de sortie
    nettoyer_dossier(output_dir)

    cmd.load(modele, "modele_base")

    # Configure la vue pour centrer et ajuster le fond
    cmd.bg_color("black")  # Défini le fond noir
    cmd.center("modele_base")  # Centrer sur le modèle
    cmd.zoom("modele_base", 2.0)  # Zoom sur le modèle avec un facteur ajustable

    fragments = obtenir_fragments_depuis_dossier(dossier_fragments)

    for fragment in fragments:
        nom_fragment = os.path.basename(fragment).replace('.pdb', '')

        # Charge le fragment
        cmd.load(fragment, nom_fragment)
        
        # Effectue la superposition
        cmd.align(nom_fragment, "modele_base")

        # Centrer et ajuster après la superposition
        cmd.center("modele_base")
        cmd.zoom("modele_base", 2.0)

        # Paramètres pour améliorer le rendu visuel
        
        cmd.set("ray_opaque_background", 0)  # Fond transparent pour l'image
        cmd.set("ray_trace_mode", 3)  # Mode de rendu (photoréaliste)
        cmd.set("cartoon_transparency", 0.2)  # Transparence du cartoon (ajustable)
        cmd.show("cartoon", "all")  # Afficher toutes les structures en mode cartoon
        cmd.color("red", "modele_base")  # Couleur rouge pour le modèle de base
        cmd.color("cyan", nom_fragment)  # Couleur cyan pour le fragment

        # Enregistre l'image en PNG
        output_image = os.path.join(output_dir, f"{nom_fragment}_superposition.png")
        cmd.ray(800, 600)  # Taille de l'image (800x600)
        cmd.png(output_image)

        # Nettoye la session PyMOL
        cmd.delete(nom_fragment)

    print(f"Les images ont été enregistrées dans le dossier '{output_dir}'.")

modele = "/Users/unluismail/Downloads/7bid_sans_h2o.pdb"  
dossier_fragments = "/Users/unluismail/Downloads/Fragments_conformes"  
output_dir = "image_superposition"  

superposer_et_enregistrer_image(modele, dossier_fragments, output_dir)
