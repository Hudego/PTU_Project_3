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

def extract_fragments_by_disorder(model, plddt_scores, threshold=70, min_consecutive=9, tolerance=5, high_score_threshold=90, min_high_score_count=4):
    fragments = []
    fragment = []
    consecutive_count = 0
    low_score_count = 0
    high_score_count = 0  # Compteur pour les scores >= 90

    for i, residue in enumerate(model.get_residues()):
        if plddt_scores[i] >= threshold:
            consecutive_count += 1
            low_score_count = 0  # Réinitialiser le compteur de basse qualité
            fragment.append(residue)
            
            # Compter les résidus avec un score >= 90
            if plddt_scores[i] >= high_score_threshold:
                high_score_count += 1

            # Vérifier si la longueur minimale pour commencer un fragment est atteinte
            if consecutive_count >= min_consecutive and len(fragment) == consecutive_count:
                # Ne pas valider le fragment encore ici, on attend de voir si la condition des scores >= 90 est remplie
                pass
        
        else:
            low_score_count += 1
            # Permettre une tolérance jusqu'à un certain nombre de résidus en dessous du seuil
            if low_score_count <= tolerance and fragment:
                fragment.append(residue)
            else:
                # Finir le fragment si la tolérance est dépassée et si les critères sont remplis
                if len(fragment) >= min_consecutive and high_score_count >= min_high_score_count:
                    fragments.append(fragment)
                # Réinitialiser les variables pour un nouveau fragment potentiel
                fragment = []
                consecutive_count = 0
                low_score_count = 0
                high_score_count = 0

    # Ajouter le dernier fragment s'il est valide
    if len(fragment) >= min_consecutive and high_score_count >= min_high_score_count:
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
        fragments = extract_fragments_by_disorder(model, plddt_scores, threshold=70, min_consecutive=9, tolerance=5)
        
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
