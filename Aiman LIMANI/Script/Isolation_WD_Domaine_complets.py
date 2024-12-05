import os
import pymol
from pymol import cmd

# Dossier contenant les fichiers PDB
dossier_entrée = r'C:\Users\Liman\.vscode\Enter'
dossier_sortie = r'C:\Users\Liman\.vscode\Enter\fragments_nettoyés'
fichier_reference = r'C:\Users\Liman\Downloads\7bid.pdb'  # Fichier PDB de référence

# Crée le dossier de sortie s'il n'existe pas
os.makedirs(dossier_sortie, exist_ok=True)

def vider_dossier_sortie():
    """Fonction pour vider le dossier de sortie"""
    for fichier in os.listdir(dossier_sortie):
        chemin_fichier = os.path.join(dossier_sortie, fichier)
        if os.path.isfile(chemin_fichier):
            os.remove(chemin_fichier)
            print(f"Fichier {chemin_fichier} supprimé.")

def superposer_et_nettoyer_pdb(fichier_pdb, fichier_reference, dossier_sortie, distance_seuil=5.0):
    """
    Superpose et nettoie un fichier PDB par rapport à un fichier de référence
    
    Args:
    - fichier_pdb (str): Chemin du fichier PDB à traiter
    - fichier_reference (str): Chemin du fichier PDB de référence
    - dossier_sortie (str): Dossier où sauvegarder le fichier nettoyé
    - distance_seuil (float): Distance maximale pour conserver un résidu
    """
    try:
        # Réinitialiser PyMOL
        cmd.reinitialize()
        
        # Charger les fichiers
        cmd.load(fichier_reference, 'proteine_reference')
        cmd.load(fichier_pdb, 'proteine_a_nettoyer')
        
        # Aligner la protéine sur la référence
        cmd.align('proteine_a_nettoyer', 'proteine_reference')
        
        # Sélectionner et supprimer les résidus trop éloignés
        # Modification de la syntaxe de sélection
        cmd.select('residus_proches', f'proteine_a_nettoyer within {distance_seuil} of proteine_reference')
        
        # Créer une nouvelle sélection avec uniquement les résidus proches
        cmd.create('proteine_nettoyee', 'residus_proches')
        
        # Nom de fichier de sortie
        nom_fichier = os.path.basename(fichier_pdb)
        fichier_sortie = os.path.join(dossier_sortie, f'proteine_nettoyee_{nom_fichier}')
        
        # Options de sauvegarde pour réduire la taille
        cmd.save(fichier_sortie, selection='proteine_nettoyee', 
                 format='pdb', 
                 quiet=1,  # Réduire la verbosité
                 partial=1)  # Ne sauvegarder que les atomes sélectionnés
        
        print(f"Structure nettoyée sauvegardée dans {fichier_sortie}")
    
    except Exception as e:
        print(f"Erreur lors du traitement de {fichier_pdb}: {e}")
    finally:
        # Nettoyer les objets
        cmd.delete('all')

def main():
    # Vider le dossier de sortie
    vider_dossier_sortie()
    
    # Liste des fichiers PDB à traiter
    fichiers_pdb = [os.path.join(dossier_entrée, f) for f in os.listdir(dossier_entrée) if f.endswith('.pdb')]
    
    # Traiter chaque fichier
    for fichier in fichiers_pdb:
        superposer_et_nettoyer_pdb(fichier, fichier_reference, dossier_sortie)

if __name__ == "__main__":
    main()
