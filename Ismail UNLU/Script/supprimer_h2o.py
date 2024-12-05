def enlever_eau_pdb(fichier_entree, fichier_sortie):
    """
    Supprime les molécules d'eau (HOH) d'un fichier PDB et sauvegarde le fichier résultant.

    :param fichier_entree: Chemin du fichier PDB d'entrée.
    :param fichier_sortie: Chemin du fichier PDB de sortie sans les molécules d'eau.
    """
    # Ouvre le fichier PDB d'entrée en lecture et le fichier de sortie en écriture.
    with open(fichier_entree, 'r') as f_in, open(fichier_sortie, 'w') as f_out:
        for ligne in f_in:  # Parcourt chaque ligne du fichier d'entrée.
            # Vérifie si la ligne n'est pas une ligne "HETATM" contenant "HOH" (molécule d'eau).
            if not ligne.startswith("HETATM") or "HOH" not in ligne:
                f_out.write(ligne)  # Si la ligne ne correspond pas à une molécule d'eau, elle est écrite.

# Chemin du fichier PDB d'entrée contenant des molécules d'eau.
fichier_pdb = "/Users/unluismail/Downloads/7bid.pdb"

# Chemin du fichier PDB de sortie où les molécules d'eau seront supprimées.
fichier_pdb_sans_eau = "/Users/unluismail/Downloads/7bid_sans_h2o.pdb"

# Appel de la fonction pour supprimer les molécules d'eau du fichier PDB.
enlever_eau_pdb(fichier_pdb, fichier_pdb_sans_eau)

# Confirmation que le fichier modifié a été sauvegardé avec succès.
print(f"Fichier modifié sans molécules d'eau sauvegardé dans : {fichier_pdb_sans_eau}")
