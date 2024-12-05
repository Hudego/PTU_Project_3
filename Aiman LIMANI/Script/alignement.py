#!/usr/bin/env python3
import os
import sys

def concatenate_fasta_files(input_folder, output_file=None):

    # Vérifier si le dossier existe
    if not os.path.isdir(input_folder):
        print(f"Erreur : Le dossier {input_folder} n'existe pas.")
        sys.exit(1)
    
    # Chercher tous les fichiers .fasta dans le dossier
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.fasta')]
    
    if not input_files:
        print(f"Aucun fichier FASTA trouvé dans le dossier {input_folder}.")
        sys.exit(1)
    
    print(f"{len(input_files)} fichiers FASTA trouvés dans le dossier {input_folder}.")
    
    # Générer le fichier de sortie si non spécifié
    if output_file is None:
        output_file = os.path.join(input_folder, "concatenated_sequences.fasta")
    
    # Dictionnaire pour stocker les séquences
    sequences = {}
    
    # Parcourir chaque fichier d'entrée
    for input_file in input_files:
        with open(input_file, 'r') as f:
            current_header = None
            current_sequence = []
            
            for line in f:
                line = line.strip()
                
                # Ligne d'en-tête
                if line.startswith('>'):
                    # Si on avait déjà un en-tête, on sauvegarde la séquence précédente
                    if current_header:
                        # Concaténer si l'identifiant existe déjà
                        if current_header in sequences:
                            sequences[current_header] += ''.join(current_sequence)
                        else:
                            sequences[current_header] = ''.join(current_sequence)
                    
                    # Réinitialiser pour le nouvel en-tête
                    current_header = line
                    current_sequence = []
                
                # Ligne de séquence
                else:
                    current_sequence.append(line)
            
            # Gérer la dernière séquence du fichier
            if current_header:
                if current_header in sequences:
                    sequences[current_header] += ''.join(current_sequence)
                else:
                    sequences[current_header] = ''.join(current_sequence)
    
    # Écrire les séquences concaténées
    with open(output_file, 'w') as out_f:
        for header, sequence in sequences.items():
            out_f.write(f"{header}\n")
            # Formater la séquence avec des sauts de ligne tous les 60 caractères
            for i in range(0, len(sequence), 60):
                out_f.write(f"{sequence[i:i+60]}\n")
    
    print(f"Fichiers concaténés avec succès. Fichier de sortie : {output_file}")
    return output_file

def main():
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage : python script.py dossier_de_fichiers_fasta [fichier_de_sortie.fasta]")
        print("Exemple : python script.py ./dossier_fasta")
        sys.exit(1)
    
    # Récupérer le dossier d'entrée et éventuellement le fichier de sortie
    input_folder = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Concaténer les fichiers FASTA dans le dossier
    concatenate_fasta_files(input_folder, output_file)

if __name__ == "__main__":
    main()
