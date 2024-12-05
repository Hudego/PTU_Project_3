import os
from pymol import cmd
import plotly.express as px
import pandas as pd
import numpy as np  # Nécessaire pour calculer le logarithme
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import shutil  # Pour copier les fichiers

def obtenir_fragments_depuis_dossier(dossier):
    """
    Récupère tous les fichiers .pdb d'un dossier donné, en excluant les fichiers correspondant aux protéines entières.
    """
    fragments = []
    for fichier in os.listdir(dossier):
        if fichier.endswith('.pdb') and 'fragment' in fichier:  # Assurez-vous que 'fragment' est dans le nom du fichier
            fragments.append(os.path.join(dossier, fichier))
    return fragments

def calculer_rmsd_et_alignes(fragment, longueur_aa_min):
    """
    Calcule le RMSD et le nombre d'atomes alignés pour un fragment donné, seulement si sa longueur en acides aminés est suffisante.
    """
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

def scatterplot_interactif_rmsd_vs_alignes(modele, dossier_fragments, dossier_conformes, longueur_aa_min=100):
    """
    Charge un modèle de référence, analyse les fragments d'un dossier, et crée un graphique 
    interactif scatterplot des log(RMSD) et du nombre d'atomes alignés. Ajoute dans un dossier les fragments
    qui répondent aux critères (log(RMSD) < 1 et au moins 400 atomes alignés).
    """
    cmd.load(modele, "modele_base")
    fragments = obtenir_fragments_depuis_dossier(dossier_fragments)

    data = []  # Liste pour stocker les informations (RMSD, atomes alignés, noms des fragments)
    fragments_conformes = []  # Liste pour stocker les fragments qui répondent aux critères

    # Créer le dossier pour les fragments conformes s'il n'existe pas
    os.makedirs(dossier_conformes, exist_ok=True)

    # Utiliser ThreadPoolExecutor pour paralléliser le calcul
    with ThreadPoolExecutor() as executor:
        futures = []
        fragment_names = []  # Stocker les noms des fragments
        with tqdm(total=len(fragments), desc='Superposition et calcul du RMSD', unit='fragment') as pbar:
            for fragment in fragments:
                futures.append(executor.submit(calculer_rmsd_et_alignes, fragment, longueur_aa_min))
                fragment_names.append(os.path.basename(fragment))  # Stocker le nom du fragment

            for fragment_name, fragment_path, future in zip(fragment_names, fragments, futures):
                rmsd, aligned = future.result()
                if rmsd is not None and aligned is not None:
                    log_rmsd = np.log10(rmsd) if rmsd > 0 else None
                    data.append({"Nom Fragment": fragment_name, "RMSD": rmsd, "Log RMSD": log_rmsd, "Atomes Alignés": aligned})
                    # Vérifier si le fragment répond aux critères
                    if log_rmsd is not None and log_rmsd < 1 and aligned >= 400:
                        fragments_conformes.append(fragment_name)
                        # Copier le fichier dans le dossier cible
                        shutil.copy(fragment_path, os.path.join(dossier_conformes, fragment_name))
                pbar.update(1)

    # Convertir les données en DataFrame pour utilisation avec Plotly
    df = pd.DataFrame(data)

    # Création du scatterplot interactif
    fig = px.scatter(
        df,
        x="Log RMSD",  # Utilisation du logarithme pour l'axe x
        y="Atomes Alignés",
        text="Nom Fragment",
        title="Scatterplot interactif: Log RMSD vs Nombre d'atomes alignés",
        labels={"Log RMSD": "Log10(RMSD)", "Atomes Alignés": "Nombre d'atomes alignés"}
    )
    fig.update_traces(marker=dict(size=10, color='blue', opacity=0.7), textposition="top center")
    fig.update_layout(
        hovermode="closest",
        template="plotly_white",
    )
    fig.show()

    # Afficher la liste des fragments conformes après le graphique
    print("\nFragments conformes aux critères (log(RMSD) < 1 et >= 400 atomes alignés) :")
    if fragments_conformes:
        for fragment in fragments_conformes:
            print(f"- {fragment}")
    else:
        print("Aucun fragment ne répond aux critères.")

    # Nettoyer la session PyMOL
    cmd.delete("all")

# Exemple d'utilisation
modele = "7bid.pdb"
dossier_fragments = "Fragments gap 30 aa + proteines"
dossier_conformes = "Fragments_conformes"  # Dossier où enregistrer les fragments conformes
scatterplot_interactif_rmsd_vs_alignes(modele, dossier_fragments, dossier_conformes, longueur_aa_min=50)



