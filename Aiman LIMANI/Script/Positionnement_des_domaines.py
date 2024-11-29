import os
import matplotlib.pyplot as plt
from collections import defaultdict

def lire_fichier_rmsd(fichier_rmsd):
    """
    Lit le fichier 'fragments_rmsd_faible.txt' et retourne un dictionnaire contenant
    les fragments alignés pour chaque protéine.
    """
    fragments_proteines = defaultdict(list)
    with open(fichier_rmsd, 'r') as f:
        next(f)  # Ignorer l'en-tête
        for ligne in f:
            proteine, fragment, rmsd = ligne.strip().split('\t')
            fragments_proteines[proteine].append(fragment)
    return fragments_proteines

def extraire_positions_de_fragment(fichier_pdb):
    """
    Extrait les positions des premiers et derniers acides aminés dans un fichier PDB de fragment.
    """
    debut, fin = None, None
    with open(fichier_pdb, 'r') as f:
        for ligne in f:
            if ligne.startswith("ATOM") and " CA " in ligne:  # Trouve les atomes CA (carbones alpha)
                resseq = int(ligne[22:26].strip())  # Récupère le numéro de séquence du résidu
                if debut is None:
                    debut = resseq  # Premier acide aminé
                fin = resseq  # Dernier acide aminé
    return debut, fin

def obtenir_positions_fragments(fragments_proteines, dossier_fragments):
    """
    Récupère les positions initiales et finales de chaque fragment aligné en lisant les fichiers PDB correspondants.
    """
    positions_fragments = defaultdict(list)
    for proteine, fragments in fragments_proteines.items():
        for fragment in fragments:
            chemin_fragment = os.path.join(dossier_fragments, f"{fragment}.pdb")
            if os.path.isfile(chemin_fragment):
                debut, fin = extraire_positions_de_fragment(chemin_fragment)
                positions_fragments[proteine].append((fragment, debut, fin))
            else:
                print(f"Fichier {chemin_fragment} introuvable.")
    return positions_fragments

def construire_graphique_domaine(positions_fragments):
    """
    Construit un graphique montrant les positions des domaines alignés pour chaque protéine.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (proteine, fragments) in enumerate(positions_fragments.items()):
        for fragment, position_debut, position_fin in fragments:
            ax.plot([position_debut, position_fin], [i, i], marker='|', color='skyblue', linewidth=4, label=proteine if i == 0 else "")

    # Paramètres du graphique
    ax.set_yticks(range(len(positions_fragments)))
    ax.set_yticklabels(positions_fragments.keys())
    ax.set_xlabel("Position dans la séquence protéique")
    ax.set_ylabel("Protéine")
    ax.set_title("Positions des domaines alignés pour chaque protéine")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Lecture du fichier RMSD et récupération des fragments alignés pour chaque protéine
fichier_rmsd = "fragments_rmsd_faible.txt"
dossier_fragments = "C:\\Users\\Liman\\.vscode\\Enter"  # Spécifiez le dossier contenant les fichiers PDB
fragments_proteines = lire_fichier_rmsd(fichier_rmsd)

# Obtenir les positions des fragments en lisant les fichiers PDB
positions_fragments = obtenir_positions_fragments(fragments_proteines, dossier_fragments)

# Construire le graphique
construire_graphique_domaine(positions_fragments)
