import os
from pymol import cmd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def obtenir_fragments_depuis_dossier(dossier):
    
    # Récupère tous les fichiers .pdb d'un dossier donné, en excluant les fichiers correspondant aux protéines entières.
    
    fragments = []
    for fichier in os.listdir(dossier):
        if fichier.endswith('.pdb') and 'fragment' in fichier:  # Assurez-vous que 'fragment' est dans le nom du fichier
            fragments.append(os.path.join(dossier, fichier))
    return fragments

def calculer_rmsd_et_alignes(fragment, longueur_aa_min):
    
    # Calcule le RMSD et le nombre d'atomes alignés pour un fragment donné, seulement si sa longueur en acides aminés est suffisante.
    
    nom_fragment = os.path.basename(fragment).replace('.pdb', '')
    cmd.load(fragment, nom_fragment)
    
    # Vérifier la longueur en acides aminés du fragment
    cmd.select(f"selection_{nom_fragment}", f"{nom_fragment} and name CA")
    longueur_aa = cmd.count_atoms(f"selection_{nom_fragment}")  # Nombre d'atomes alignés (carbones alpha)

    if longueur_aa >= longueur_aa_min:
        rmsd, atomes_alignes = cmd.align(nom_fragment, "modele_base")[0:2]
        cmd.delete(nom_fragment)  # Nettoyage pour éviter la surcharge dans PyMOL
        return rmsd, atomes_alignes
    else:
        cmd.delete(nom_fragment)  # Nettoyage
        return None, None

def scatterplot_rmsd_vs_alignes(modele, dossier_fragments, longueur_aa_min=40):
    cmd.load(modele, "modele_base")
    fragments = obtenir_fragments_depuis_dossier(dossier_fragments)

    rmsd_values = []
    aligned_counts = []

    # Utiliser ThreadPoolExecutor pour paralléliser le calcul
    with ThreadPoolExecutor() as executor:
        futures = []
        with tqdm(total=len(fragments), desc='Superposition et calcul du RMSD', unit='fragment') as pbar:
            for fragment in fragments:
                futures.append(executor.submit(calculer_rmsd_et_alignes, fragment, longueur_aa_min))

            for future in futures:
                rmsd, aligned = future.result()
                if rmsd is not None and aligned is not None:
                    rmsd_values.append(rmsd)
                    aligned_counts.append(aligned)
                pbar.update(1)

    # Création du scatterplot
    plt.figure(figsize=(10, 6))
    plt.scatter(np.log(rmsd_values), aligned_counts, c='blue', alpha=0.7, edgecolors='w', s=80)
    plt.xlabel('Log(RMSD)')
    plt.ylabel('Number of Aligned Atoms')
    plt.title('RMSD vs Number of Aligned Atoms')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Nettoyer la session PyMOL
    cmd.delete("all")

# Exemple d'utilisation
modele = "7bid.pdb"
dossier_fragments = "Fragments"
scatterplot_rmsd_vs_alignes(modele, dossier_fragments, longueur_aa_min=50)

