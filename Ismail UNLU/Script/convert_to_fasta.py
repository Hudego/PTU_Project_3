"""
essaie non réussi car pas de WD dans l'alignement Mafft
version:
python: 3.12.7

"""

from Bio.PDB import PDBParser  # Importer le module pour analyser les fichiers PDB.
from Bio.Seq import Seq  # Pour manipuler des séquences biologiques.
from Bio.SeqRecord import SeqRecord  # Pour représenter des séquences avec des métadonnées.
from Bio import SeqIO  # Pour écrire les séquences dans un fichier FASTA.
import os  # Pour la gestion des fichiers et des répertoires.

def extract_sequences(pdb_folder, output_fasta):
    """
    Extrait les séquences d'acides aminés des fichiers PDB dans un dossier donné
    et les enregistre dans un fichier FASTA.

    :param pdb_folder: Chemin du dossier contenant les fichiers PDB.
    :param output_fasta: Nom du fichier FASTA de sortie.
    """
    parser = PDBParser(QUIET=True)  # Initialiser un parseur PDB sans afficher d'avertissements.
    records = []  # Liste pour stocker les objets SeqRecord des séquences extraites.

    # Parcourir tous les fichiers du dossier spécifié.
    for pdb_file in os.listdir(pdb_folder):
        if pdb_file.endswith(".pdb"):  # Vérifier si le fichier a une extension .pdb.
            # Charger la structure PDB depuis le fichier.
            structure = parser.get_structure(pdb_file, os.path.join(pdb_folder, pdb_file))
            
            # Parcourir les modèles, chaînes, et résidus dans la structure PDB.
            for model in structure:
                for chain in model:
                    seq = ""  # Initialiser une chaîne vide pour stocker la séquence.
                    for residue in chain:
                        # Vérifier si le résidu possède un atome alpha-carbone (CA), signe qu'il s'agit d'un acide aminé.
                        if residue.has_id("CA"):  
                            seq += residue.resname  # Ajouter le nom du résidu à la séquence.
                    
                    # Si une séquence a été construite pour la chaîne, la stocker comme SeqRecord.
                    if seq:
                        seq_record = SeqRecord(Seq(seq), id=f"{pdb_file}_{chain.id}")
                        records.append(seq_record)  # Ajouter l'objet SeqRecord à la liste.

    # Écrire toutes les séquences extraites dans un fichier FASTA.
    SeqIO.write(records, output_fasta, "fasta")
    print(f"Fichier FASTA généré : {output_fasta}")  # Confirmer que le fichier FASTA a été généré.

# Spécifier le dossier contenant les fichiers PDB et le fichier FASTA de sortie.
pdb_folder = "/Users/unluismail/Downloads/fragments_nettoyes"
output_fasta = "fragmentfasta2"

# Appeler la fonction pour extraire les séquences et générer le fichier FASTA.
extract_sequences(pdb_folder, output_fasta)

