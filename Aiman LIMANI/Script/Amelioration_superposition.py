import os
from pymol import cmd
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def obtenir_fragments_depuis_dossier(dossier):
    """
    Récupère tous les fichiers .pdb d'un dossier donné, en excluant les fichiers correspondant aux protéines entières.
    """
    fragments_par_proteine = defaultdict(list)
    for fichier in os.listdir(dossier):
        if fichier.endswith('.pdb') and 'fragment' in fichier:
            nom_proteine = fichier.split('_')[0]
            fragments_par_proteine[nom_proteine].append(os.path.join(dossier, fichier))
    return fragments_par_proteine

def calculer_rmsd(fragment, longueur_aa_min):
    """
    Calcule le RMSD pour un fragment donné, seulement si sa longueur en acides aminés est suffisante.
    """
    nom_fragment = os.path.basename(fragment).replace('.pdb', '')
    cmd.load(fragment, nom_fragment)
    
    cmd.select(f"selection_{nom_fragment}", f"{nom_fragment} and name CA")
    longueur_aa = cmd.count_atoms(f"selection_{nom_fragment}")
    
    if longueur_aa >= longueur_aa_min:
        rmsd = cmd.align(nom_fragment, "modele_base")[0]
        return rmsd, nom_fragment
    else:
        return None, nom_fragment

def superposer_et_enregistrer_rmsd(modele, dossier_fragments, seuil_rmsd=2.5, longueur_aa_min=30):
    cmd.load(modele, "modele_base")
    fragments_par_proteine = obtenir_fragments_depuis_dossier(dossier_fragments)
    fragments_rmsd_faible = []
    proteines_sans_rmsd_faible = []

    with ThreadPoolExecutor() as executor:
        futures = []
        total_nombre_fragments = sum(len(fragments) for fragments in fragments_par_proteine.values())
        
        with tqdm(total=total_nombre_fragments, desc='Superposition et calcul du RMSD', unit='fragment') as pbar:
            for fragments in fragments_par_proteine.values():
                for fragment in fragments:
                    futures.append(executor.submit(calculer_rmsd, fragment, longueur_aa_min))

            for future in futures:
                result = future.result()
                if result is not None:
                    rmsd, nom_fragment = result
                    if rmsd is not None:
                        proteine = nom_fragment.split('_')[0]
                        if rmsd < seuil_rmsd:
                            fragments_rmsd_faible.append(f"{proteine}\t{nom_fragment}\t{rmsd:.2f}")
                        else:
                            proteines_sans_rmsd_faible.append(proteine)
                    pbar.update(1)

    # Enregistrement des résultats dans des fichiers texte
    with open("fragments_rmsd_faible.txt", "w") as fichier_rmsd_faible:
        fichier_rmsd_faible.write("Protéine\tFragment\tRMSD\n")
        fichier_rmsd_faible.write("\n".join(fragments_rmsd_faible))
    
    with open("proteines_sans_rmsd_faible.txt", "w") as fichier_sans_rmsd_faible:
        fichier_sans_rmsd_faible.write("Protéines sans fragments RMSD < {:.2f}\n".format(seuil_rmsd))
        fichier_sans_rmsd_faible.write("\n".join(set(proteines_sans_rmsd_faible)))

    print("Résultats enregistrés dans 'fragments_rmsd_faible.txt' et 'proteines_sans_rmsd_faible.txt'.")

# Exemples d'utilisation
modele = r"C:\Users\Liman\Downloads\7bid.pdb"
dossier_fragments = r"C:\Users\Liman\.vscode\Enter"
superposer_et_enregistrer_rmsd(modele, dossier_fragments, longueur_aa_min=50)
