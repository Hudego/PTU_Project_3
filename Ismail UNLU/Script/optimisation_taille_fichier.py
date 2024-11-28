from PIL import Image

# Ouvre l'image PNG
img = Image.open("/Users/unluismail/Downloads/image_combinee_grille_noms.png")
img = img.convert("P", palette=Image.ADAPTIVE, colors=256)

# Sauvegarde en optimisant la compression sans perte
img.save("image_optimisee.png", optimize=True)
