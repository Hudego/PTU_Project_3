import os
from pymol import cmd
import matplotlib.pyplot as plt
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # Importer tqdm pour la barre de chargement

def obtenir_fragments_depuis_dossier(dossier):
    """
    Récupère tous les fichiers .pdb d'un dossier donné, en excluant les fichiers correspondant aux protéines entières.
    """
    fragments_par_proteine = defaultdict(list)
    for fichier in os.listdir(dossier):
        if fichier.endswith('.pdb'):
            # Exclure les fichiers correspondant à des protéines entières
            if 'fragment' in fichier:  # Assurez-vous que 'fragment' est dans le nom du fichier
                nom_proteine = fichier.split('_')[0]
                fragments_par_proteine[nom_proteine].append(os.path.join(dossier, fichier))
    return fragments_par_proteine

def calculer_rmsd(fragment, longueur_aa_min):
    """
    Calcule le RMSD pour un fragment donné, seulement si sa longueur en acides aminés est suffisante.
    """
    nom_fragment = os.path.basename(fragment).replace('.pdb', '')
    cmd.load(fragment, nom_fragment)
    
    # Vérifier la longueur en acides aminés du fragment
    cmd.select(f"selection_{nom_fragment}", f"{nom_fragment} and name CA")  # Sélectionne les carbones alpha
    longueur_aa = cmd.count_atoms(f"selection_{nom_fragment}")  # Compte les atomes sélectionnés (carbones alpha)
    
    if longueur_aa >= longueur_aa_min:
        rmsd = cmd.align(nom_fragment, "modele_base")[0]
        return rmsd, nom_fragment
    else:
        # Si la longueur est insuffisante, on retourne None pour signaler l'absence d'alignement
        return None, nom_fragment

def superposer_et_graphique_rmsd(modele, dossier_fragments, seuil_rmsd=1.0, longueur_aa_min=50):
    cmd.load(modele, "modele_base")
    fragments_par_proteine = obtenir_fragments_depuis_dossier(dossier_fragments)
    comptage_fragments = defaultdict(int)
    total_fragments = defaultdict(int)  # Dictionnaire pour compter le total de fragments par protéine

    # Utiliser ThreadPoolExecutor pour paralléliser le calcul de RMSD
    with ThreadPoolExecutor() as executor:
        futures = []
        total_nombre_fragments = sum(len(fragments) for fragments in fragments_par_proteine.values())
        
        # Barre de chargement générale pour l'ensemble du processus
        with tqdm(total=total_nombre_fragments, desc='Superposition et calcul du RMSD', unit='fragment') as pbar:
            for fragments in fragments_par_proteine.values():
                for fragment in fragments:
                    futures.append(executor.submit(calculer_rmsd, fragment, longueur_aa_min))

            for future in futures:
                result = future.result()
                if result is not None:
                    rmsd, nom_fragment = result
                    if rmsd is not None:  # Vérifie si l'alignement a été effectué
                        proteine = nom_fragment.split('_')[0]
                        if rmsd < seuil_rmsd:
                            comptage_fragments[proteine] += 1
                        total_fragments[proteine] += 1  # Compter le total de fragments pour chaque protéine
                    pbar.update(1)  # Mettre à jour la barre de progression pour chaque fragment traité

    cmd.orient()

    # Création du graphique pour le nombre de fragments avec RMSD faible
    plt.figure(figsize=(10, 6))
    proteines = list(comptage_fragments.keys())
    nombres_fragments = [comptage_fragments[proteine] for proteine in proteines]

    plt.bar(proteines, nombres_fragments, color='skyblue')
    plt.xlabel('Protéines')
    plt.ylabel('Nombre de fragments avec RMSD faible')
    plt.title(f'Nombre de fragments avec RMSD < {seuil_rmsd} Å par protéine')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # Affichage des résultats
    for proteine in proteines:
        count = comptage_fragments[proteine]
        total_count = total_fragments[proteine]
        moyenne = count / total_count if total_count > 0 else 0
        print(f"Nombre de fragments avec un RMSD < {seuil_rmsd} Å pour {proteine}: {count}")
        print(f"Moyenne des fragments superposés pour {proteine}: {moyenne:.2f}")

# Exemples d'utilisation
modele = r"C:\Users\Liman\Downloads\7bid.pdb"
dossier_fragments = r"C:\Users\Liman\.vscode\Enter"
superposer_et_graphique_rmsd(modele, dossier_fragments, longueur_aa_min=50)
