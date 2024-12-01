def enlever_eau_pdb(fichier_entree, fichier_sortie):
  
    with open(fichier_entree, 'r') as f_in, open(fichier_sortie, 'w') as f_out:
        for ligne in f_in:
            # Garde les lignes qui ne contiennent pas "HOH"
            if not ligne.startswith("HETATM") or "HOH" not in ligne:
                f_out.write(ligne)

fichier_pdb = "/Users/unluismail/Downloads/7bid.pdb"
fichier_pdb_sans_eau = "/Users/unluismail/Downloads/7bid_sans_h2o.pdb"

enlever_eau_pdb(fichier_pdb, fichier_pdb_sans_eau)

print(f"Fichier modifié sans molécules d'eau sauvegardé dans : {fichier_pdb_sans_eau}")
