from PIL import Image, ImageDraw, ImageFont
import os

def assembler_images_en_grille_avec_noms(dossier_images, sortie, max_par_ligne=20, taille_texte=20):
    """
    Assemble toutes les images d'un dossier dans une grille avec les noms des fragments ajoutés.
    
    Arguments :
    - dossier_images : Chemin vers le dossier contenant les images PNG.
    - sortie : Chemin vers l'image combinée à générer (fichier .png).
    - max_par_ligne : Nombre maximum d'images par ligne.
    - taille_texte : Taille de la police pour les noms des fragments.
    """
    # Récupère la liste des images PNG dans le dossier
    images = [os.path.join(dossier_images, f) for f in os.listdir(dossier_images) if f.endswith('.png')]
    images.sort()  # Tri les images par nom pour un ordre cohérent

    if not images:
        print("Aucune image trouvée dans le dossier.")
        return

    # Charge toutes les images
    image_objs = [Image.open(img) for img in images]
    noms_images = [os.path.basename(img).replace('.png', '') for img in images]

    # Dimensions des images (on suppose que toutes les images ont la même hauteur)
    largeur_image = max(img.width for img in image_objs)
    hauteur_image = max(img.height for img in image_objs)

    # Calcule la grille
    lignes = (len(image_objs) + max_par_ligne - 1) // max_par_ligne  # Nombre total de lignes
    largeur_totale = largeur_image * max_par_ligne
    hauteur_totale = hauteur_image * lignes

    # Créé une nouvelle image vide avec un fond noir
    image_finale = Image.new("RGB", (largeur_totale, hauteur_totale), "black")
    draw = ImageDraw.Draw(image_finale)

    # Charge une police par défaut
    try:
        font = ImageFont.truetype("arial.ttf", taille_texte)  # Utilise Arial si disponible
    except IOError:
        font = ImageFont.load_default()  # Police par défaut si Arial n'est pas disponible

    # Colle les images dans la grille avec les noms des fragments
    x_offset, y_offset = 0, 0
    for idx, (img, nom) in enumerate(zip(image_objs, noms_images)):
        image_finale.paste(img, (x_offset, y_offset))

        # Ajoute le nom en haut à gauche de l'image
        draw.text((x_offset + 5, y_offset + 5), nom, fill="white", font=font)

        # Passe à l'image suivante
        x_offset += largeur_image

        # Si la ligne est remplie, passe à la suivante
        if (idx + 1) % max_par_ligne == 0:
            x_offset = 0
            y_offset += hauteur_image

    # Sauvegarde l'image finale
    image_finale.save(sortie)
    print(f"Image combinée avec noms sauvegardée dans : {sortie}")

dossier_images = "/Users/unluismail/Downloads/image_superposition"  
sortie = "image_combinee_grille_noms.png"  

assembler_images_en_grille_avec_noms(dossier_images, sortie, max_par_ligne=20, taille_texte=20)
