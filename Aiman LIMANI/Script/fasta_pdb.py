from Bio import PDB
import os
import argparse

def pdb_to_fasta(pdb_file):
    """
    Convertit un fichier PDB en séquence FASTA.
    
    Args:
        pdb_file (str): Chemin vers le fichier PDB à convertir
    
    Returns:
        str: Séquence au format FASTA
    """
    # Initialiser le parser PDB
    parser = PDB.PDBParser(QUIET=True)
    
    try:
        # Charger la structure
        structure = parser.get_structure('protein', pdb_file)
        
        # Extraire la séquence
        ppb = PDB.PPBuilder()
        sequences = []
        
        for pp in ppb.build_peptides(structure):
            seq = pp.get_sequence()
            sequences.append(str(seq))
        
        # Si plusieurs chaînes, on les combine
        full_sequence = ''.join(sequences)
        
        # Générer le nom du fichier FASTA basé sur le nom du fichier PDB
        base_name = os.path.splitext(os.path.basename(pdb_file))[0]
        
        # Créer la chaîne FASTA
        fasta_string = f">{base_name}\n{full_sequence}"
        
        return fasta_string
    
    except Exception as e:
        print(f"Erreur lors du traitement du fichier {pdb_file}: {e}")
        return None

def convert_multiple_pdbs(input_path, output_dir=None):
    """
    Convertit un ou plusieurs fichiers PDB en FASTA.
    
    Args:
        input_path (str): Chemin vers un fichier PDB ou un répertoire contenant des PDB
        output_dir (str, optional): Répertoire de sortie pour les fichiers FASTA
    """
    # Créer le répertoire de sortie si non spécifié
    if output_dir is None:
        output_dir = os.path.dirname(input_path) or '.'
    os.makedirs(output_dir, exist_ok=True)
    
    # Vérifier si c'est un fichier ou un répertoire
    if os.path.isfile(input_path):
        files_to_process = [input_path]
    else:
        # Trouver tous les fichiers PDB dans le répertoire
        files_to_process = [
            os.path.join(input_path, f) 
            for f in os.listdir(input_path) 
            if f.lower().endswith('.pdb')
        ]
    
    # Compteur pour suivre le nombre de conversions
    conversion_count = 0
    
    # Traiter chaque fichier
    for pdb_file in files_to_process:
        fasta_content = pdb_to_fasta(pdb_file)
        
        if fasta_content:
            # Générer le nom du fichier de sortie
            base_name = os.path.splitext(os.path.basename(pdb_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}.fasta")
            
            # Écrire le contenu FASTA
            with open(output_file, 'w') as f:
                f.write(fasta_content)
            
            print(f"Converti {pdb_file} en {output_file}")
            conversion_count += 1
    
    print(f"Conversion terminée. Total de fichiers convertis : {conversion_count}")

def main():
    """
    Point d'entrée principal du script avec gestion des arguments
    """
    parser = argparse.ArgumentParser(description='Convertir des fichiers PDB en FASTA')
    parser.add_argument('input', help='Chemin vers un fichier PDB ou un répertoire contenant des PDB')
    parser.add_argument('-o', '--output', help='Répertoire de sortie pour les fichiers FASTA')
    
    args = parser.parse_args()
    
    convert_multiple_pdbs(args.input, args.output)

if __name__ == '__main__':
    main()

# Exemple d'utilisation :
# python convert_pdb_to_fasta.py chemin/vers/fichier.pdb
# python convert_pdb_to_fasta.py chemin/vers/repertoire_pdb -o chemin/vers/repertoire_fasta