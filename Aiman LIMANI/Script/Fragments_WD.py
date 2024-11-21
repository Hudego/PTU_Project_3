import os
import pandas as pd
import requests
from Bio import PDB

# Chemin du fichier Excel
df = pd.read_excel("C:/Users/Liman/.vscode/Enter/WD_protein_list.xlsx")


# Supprimer les anciens fichiers de fragments
def remove_existing_fragments():
    for filename in os.listdir():
        if "fragment_" in filename and filename.endswith(".pdb"):
            os.remove(filename)
            print(f"Fichier supprimé : {filename}")

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
                    plddt_scores.append(atom.get_bfactor())  # Le score pLDDT est dans le champ B-factor
                    break  # Un seul atome par résidu suffit pour obtenir le score pLDDT
    return plddt_scores

# Fonction pour découper en fragments selon pLDDT avec tolérance
def extract_fragments_by_disorder(model, plddt_scores, threshold=70, tolerance=5):
    fragments = []
    fragment = []
    low_score_count = 0  # Compteur pour suivre les résidus en dessous du seuil
    
    for i, residue in enumerate(model.get_residues()):
        if plddt_scores[i] < threshold:
            low_score_count += 1
            if low_score_count >= tolerance:
                # Finir le fragment actuel
                if fragment:
                    fragments.append(fragment)
                    fragment = []
                low_score_count = 0  # Réinitialiser le compteur
        else:
            low_score_count = 0  # Réinitialiser le compteur si on est au-dessus du seuil
            fragment.append(residue)
    
    # Ajouter le dernier fragment si non vide
    if fragment:
        fragments.append(fragment)
    
    return fragments

# Supprimer les fichiers de fragments existants avant de commencer
remove_existing_fragments()

# Initialiser les outils PDB
parser = PDB.PDBParser(QUIET=True)
io = PDB.PDBIO()

# Parcourir les protéines dans le fichier et traiter chaque structure
for uniprot_id in df['code']:
    pdb_file = download_alphafold_structure(uniprot_id)
    if pdb_file:
        plddt_scores = extract_plddt_scores(pdb_file)  # Extraire les scores pLDDT
        structure = parser.get_structure(uniprot_id, pdb_file)
        model = structure[0]  # Utilisation du premier modèle
        fragments = extract_fragments_by_disorder(model, plddt_scores, threshold=70, tolerance=5)
        
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
