# PTU_Project_3

Bloc 1 : Prise en main et calcul du nombre moyen de repeats WD par protéines.
Objectif : Estimer le nombre moyen de repeats WD par protéine dans les données disponibles pour déterminer combien de repeats forment un domaine WD.
Méthode : 
-Utilisation des données UniProt pour récupérer le nombre total de repeats WD.
-Extraction des informations importantes dans le fichier Excel.
-Identification rapide des protéines à retirer pour le calcul (Protéines trop grosses, nombre incohérent de repeats, …)
-Utilisation de pandas et écriture d’un script python pour manipuler les données du fichier Excel WD_extracted_data.xlsx et filtrer les protéines en fonction des critères définis.
-Calculer une première moyenne ne prenant pas en compte les protéines avec plusieurs domaines.
Script Python (3.12.7) :
![image](https://github.com/user-attachments/assets/2b0bf226-25ef-48ac-89b8-042906d6d100)
![image](https://github.com/user-attachments/assets/215bfe0c-a777-4c4c-b92a-9daef99e60f8)

Remarque :Pour exécuter le programme, le fichier Excel et le script doivent se trouver dans le même dossier.
 J'ai utilisé Visual Studio Code (version 1.95.1) pour exécuter mon script Python.
Résultats observés :
 Avec ce script, on trie un certain nombre de protéines qu’on enlève pour calculer la moyenne. On obtient alors une moyenne de 7 repeats par domaine WD en ayant filtré au total 66 protéines.
Conclusion : La moyenne obtenu est assez cohérente car on s’attendait à un nombre de blade entre 4 et 8 environs. Néanmoins, certains problèmes sont assez évidents. Déjà, ce script ne prend pas en compte les protéines qui ont plusieurs domaines WD (ce qui multiplie donc le nombre de repeats sans pour autant que ce soit une erreur). Par la suite, il faudrait identifier manuellement les multi-domaines et faire une moyenne non pas sur le nombre de protéines, mais sur le nombre total de domaines pour avoir une estimation bien plus juste et précise.
Je n’ai également pas réussi à afficher le résultat dans des colonnes différentes pour le fichier csv. Ainsi, je resterais sur un format Excel pour le prochain script pour éviter d’avoir des problèmes de conversions.

Personne ayant travaillé sur le bloc : Hugo Mutschler, 20-21 octobre 2024


Bloc 2 : Identification des protéines avec plusieurs domaines WD et affinage de la moyenne.
Objectif : Identifier les protéines possédant plusieurs domaines WD pour ajuster le calcul de la moyenne et faire un script plus cohérent. Par la suite, l’objectif est de déterminer le nombre de de domaines WD par protéines en utilisant cette moyenne.
Méthode :
-Visualisation des protéines mal annotés en utilisant le schéma des 280 protéines (WD_map.png).
-Visualisation des structures 3D de certaines protéines via AlphaFold pour vérifier le nombre de domaine WD. On cherche le nombre de structures en forme de « donuts ». On vérifie les protéines qui semblent mal annotées avec seulement 1,2 ou 3 repeats et celles qui semblent avoir plusieurs domaines (+ de 8 repeats)
-Création d’une liste de protéines à plusieurs domaines en fonction des annotations UniProt et de la visualisation des structures. Pour gagner du temps, on part du principe que les mêmes familles de protéines ont le même nombre de domaines, ce qui est très souvent le cas.
-Recherche bibliographique pour avoir une idée plus précise du résultat attendu sur le nombre de repeats par domaine.
-Création d’un nouveau script Python plus cohérent, et qui prend en compte les protéines de notre liste avec plusieurs domaines WD. Le script renverra un fichier avec chaque protéine, leurs nombres de domaines, et leurs nombre moyen de repeatWD.

Liste des protéines avec plusieurs domaines (visualisation AlphaFold):
-EMAL5,6 = 6 domaines (x2) -APAF = 2 domaines  -CFA = 2 domaines (x4) -TEP1 = 3 domaines -STB5L = 2 domaines -STXB5 = 2 domaines -CF251 = 2 domaines -L2GL = 2 domaines (x2) -PWP2 = 2 domaines -ELP2 = 2 domaines 39 -UTP4 = 2 domaines -NWD1 = 2 domaines -EMAL2,1 = 2 domaines (x2) -TBL3 = 2 domaines -GEMI5 = 2 domaines -MABP1 = 2 domaines -WDR90 = 4 domaines -WDR6 = 3 domaines -WDR3 = 2 domaines -WDR36 = 2 domaines -WDR64 = 2 domaines -WDR62 = 2 domaines -WDR27 = 2 domaines -WDR11 = 2 domaines -DMX = pas présent dans le fichier Excel et pas prédite par AlphaFold.
On observe que la plupart des protéines à plusieurs domaines ont 2 domaines. On observe également la protéine EMAL5 et EMAL6 qui sont assez différentes des autres avec un total de 6 domaines WD dans leurs structures.

On peut refaire une moyenne en prenant en compte les protéines avec plusieurs domaines WD :
D’après les annotations UniProt et le fichier Excel, on a : 2131 WD
On a au total 280 protéines dont 24 protéines qui ont plus que 1 domaines, ce qui fait 280-24 protéines avec 1 domaine, soit 256 protéines avec 1 domaines.
Si on rajoute les protéines qui ont plusieurs domaines, ça fait 72 domaines + 256 domaines = 328 domaines pour nos 280 protéines.
On fait la moyenne pour obtenir le nombre de repeatWD par domaine : 2131 / 328 = ~ 6,5 repeats par domaines WD.
Recherche bibliographique : 
Les bêta-propeller les plus communs contiennent généralement 7 ou 8 pales. 
Source: Jain BP, Pandey S. WD40 Repeat Proteins: Signalling Scaffold with Diverse Functions. Protein J. 2018 Oct;37(5):391-406. doi: 10.1007/s10930-018-9785-7. PMID: 30069656.

Remarques supplémentaires :
Après vérification sur plusieurs protéines en utilisant AlphaFold, il semblerait que les protéines qui ont une annotation avec des oublis de repeats ne contiennent à chaque fois qu’un seul domaine. On va ainsi faire un script avec les règles suivantes :
-Toutes les protéines ont 1 domaines, sauf celles qu’on a vérifié manuellement. 
-On demande au script de nous faire un fichier Excel avec sur 1 colonne le nom des protéines, sur 1 colonne le nombre de domaines, et sur 1 colonne le nombre de repeats.
-On utilise une moyenne de 7 repeats par domaine pour faciliter les calculs et pour prendre un résultat se trouvant entre la bibliographie et proche de ce qu’on a trouvé en calculant la moyenne.
-On retire les protéines DMX car elles ne sont pas prédites par AlphaFold et sont absente du fichier Excel

Script Python (3.12.7) :
![image](https://github.com/user-attachments/assets/df5760b9-186e-4f6d-b2a8-29ad7dc8482c)
Remarques : Le fichier Excel obtenu est visible dans le dossier sous le nom « Domaines_WD_par_protéines »

Conclusion :
Ce script nous donne un fichier Excel avec chaque protéine, leurs nombres de domaines, et leurs nombres de repeats moyens. Il est possible de vérifier chaque protéine avec AlphaFold, et le résultat est très souvent correct ou très proche de la réalité.
Une moyenne se situant entre 6,5 et 7 repeats par domaine semble donc être juste et utilisable pour la suite de nos opérations.

Personne ayant travaillé sur le bloc : Hugo Mutschler, 28-31 octobre 2024



Bloc 3: Création d’une librairie de fragments de protéines humaines ayant un domaine WD

Objectif: Récupérer la structure prédites alphafold de protéines ayant un domaine WD et les fragmenter en fonction de leur score PLDDT.

Méthode:

●	Utilisation des id PDB de chaque protéine pour les prédire avec AlphaFold.
●	Automatisation du processus de prédiction des protéines présentes dans un fichier Excel.
●	Lecture des fichiers PDB des structures prédites et analyse des scores de PLDDT (colonne B-Factor).
●	Fragmentation des structures en fonction du score PLDDT.
●	Création de fichier individuels pour chaque structure/fragment obtenu

Script Python pour l’automatisation  (3.12.2)
import pandas as pd
import requests
from Bio import PDB

# Charger le fichier Excel
excel_file = r"C:\Users\Liman\OneDrive\Desktop\WD_protein_list.xlsx"  
df = pd.read_excel(excel_file)


    # Fonction pour télécharger les structures AlphaFold
def download_alphafold_structure(uniprot_id):
    url = f'https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb'
    response = requests.get(url)
    if response.status_code == 200:
        filename = f'{uniprot_id}.pdb'
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Téléchargement réussi pour {uniprot_id}")
        return filename
    else:
        print(f"Structure non trouvée pour {uniprot_id}")
        return None

    # Fonction pour extraire les scores pLDDT depuis le fichier PDB
def extract_plddt_scores(pdb_file):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('protein', pdb_file)
    plddt_scores = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    plddt_scores.append(atom.get_bfactor())  # Le score pLDDT est stocké dans le champ B-factor
                    break  # Un seul atome par résidu suffit pour obtenir le score pLDDT
    return plddt_scores

    # Fonction pour découper en fragments selon pLDDT
def extract_fragments_by_disorder(model, plddt_scores, threshold=70):
    fragments = []
    fragment = []
    for i, residue in enumerate(model.get_residues()):
        if plddt_scores[i] < threshold:
            if fragment:
                fragments.append(fragment)
                fragment = []
        else:
            fragment.append(residue)
    if fragment:
        fragments.append(fragment)
    return fragments

    # Parcourir les protéines dans le fichier et traiter chaque structure
parser = PDB.PDBParser(QUIET=True)
io = PDB.PDBIO()

for uniprot_id in df['code']:
    pdb_file = download_alphafold_structure(uniprot_id)
    if pdb_file:
        plddt_scores = extract_plddt_scores(pdb_file)  # Extraire les scores pLDDT
        structure = parser.get_structure(uniprot_id, pdb_file)
        model = structure[0]  # Utilisation du premier modèle
        fragments = extract_fragments_by_disorder(model, plddt_scores)
       
        # Sauvegarder chaque fragment
        for i, fragment in enumerate(fragments):
            # Créer une structure temporaire pour le fragment
            fragment_structure = PDB.Structure.Structure(f"{uniprot_id}_fragment_{i + 1}")
            fragment_model = PDB.Model.Model(0)
            fragment_chain = PDB.Chain.Chain("A")
            fragment_structure.add(fragment_model)
            fragment_model.add(fragment_chain)
            for residue in fragment:
                fragment_chain.add(residue)

            # Sauvegarder la structure du fragment
            io.set_structure(fragment_structure)
            io.save(f'{uniprot_id}_fragment_{i + 1}.pdb')

print("Traitement terminé pour toutes les protéines.")
Résultats observés:

Le programme nous permet d’avoir les fragments de chaque protéine, un total de 2551 fragments est observé pour 280 protéines.

Conclusion: 

Le programme nous permet de fragmenter les protéines, mais nécessite encore une étape de vérification de la qualité des fragments générés. 

Personne ayant travaillé sur le bloc : Aiman Limani, Ismail Unlu ; 20-22 octobre




Bloc 4 : Superposition des fragments obtenus sur un model de beta-propeller a fin de verifier l'annotation Uniprot .
Objectif: Superposer les fragments obtenus des structures prédites par rapport à un modèle de beta-propeller afin de retrouver le nombre moyen de WD repeat des protéines humaines.
Méthode:
●	Choix d’un modèle de beta-propeller a 7 blades ( moyenne obtenue par l’annotation de Hugo). Id beta-propeller
●	utilisation  de conda (24.1.2)
conda create -n pymol-env python=3.8 
conda activate pymol-env
conda install -c schrodinger pymol
cd C:\Users\Liman\.vscode\Enter
python "superposition fragments-Modele.py"
conda install matplotlib

●	script python  pour automatiser les superposition des fragments au modèle par PyMol
●	Analyse et mesure du nombre de fragments superposé ayant un bon score RMSD pour chaque protéine, un score RMSD faible signifié une bonne similarité et superposition
●	affichage d’un graphique nous donnant le nombre de fragments bien aligné par protéine

Script Python pour l’automatisation  (3.12.2)
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

def calculer_rmsd(fragment):
    """
    Calcule le RMSD pour un fragment donné.
    """
    nom_fragment = os.path.basename(fragment).replace('.pdb', '')
    cmd.load(fragment, nom_fragment)
    rmsd = cmd.align(nom_fragment, "modele_base")[0]
    return rmsd, nom_fragment

def superposer_et_graphique_rmsd(modele, dossier_fragments, seuil_rmsd=1.0):
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
                    futures.append(executor.submit(calculer_rmsd, fragment))

   for future in futures:
                rmsd, nom_fragment = future.result()
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
superposer_et_graphique_rmsd(modele, dossier_fragments)





Résultats observés:
résultats des superpositions trop imparfait et inutilisables ( ex: des protéines avec 1 ou 2 fragments aligné et certaines à 50 fragments aligné)


Conclusion:
En superposant les fragments créés avec le beta-propeller et en gardant seulement ceux avec un score RMSD faible on pense garder que les partie/fragments qui correspondent au beta-propeller. Cependant  les résultats restent trop aberrants et pas utilisables, le code nécessite des améliorations ou une autre approche est à tester, nous avons utilisé un base de 280 protéines qui peuvent avoir un ou plusieur domaine WD c’est pour cela qu’il faut réaliser à nouveau un test avec les 256 proteines isolé par hugo qui possèdent un seul domaine pour permettant d’avoir une distribution plus équitable et nous permettant de mieux comparer les protéines entre elles et leurs fragments.

Personne ayant travaillé sur le bloc: Aiman Limani, 1-5 novembre
Bloc 5-6 Alignez les séquences avec ces nouvelles limites pour tenter de mieux redéfinir les repeats WD et Proposer de nouvelles annotations prenant en compte l’alignement de séquence et de structure:
Objectif: Redéfinir les repeats WD et proposer des annotations mises à jour.
Méthode:
Nous devons d’abord préparer les séquences correspondant aux nouvelles limites des repeats WD et les compiler dans un fichier fasta.
Pour cela nous allons utiliser Jalview et l’outil MAFFT plus précisément car il gère des séquences divergentes ou contenant des motifs répétitifs, comme les repeats WD.
A la suite de l'alignement des séquences nous devons analyser les résultats obtenus, pour cela nous devons activer la coloration par conservation pour identifier les motifs conserver. Pour cette tâche nous devons regarder sur les différentes séquences afin de trouver des motifs qui correspondent à des éléments spécifiques des repeat WD.
Ensuite, le logiciel Jalview nous permet d’ajouter de nouvelle annotation en effet, Après superposition de structures et l’alignement de séquences le but est de trouver de nouvelles annotations afin de montrer les nouveaux motifs.
Finalement nous devons comparer les séquences de bases avec nos nouvelles séquences afin d’en tirer les conclusions.
Ismail Unlu



