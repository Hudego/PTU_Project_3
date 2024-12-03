import os
import matplotlib.pyplot as plt
from collections import defaultdict
import csv

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

def obtenir_positions_fragments(dossier_fragments):
    """
    Récupère les positions initiales et finales de chaque fragment en lisant les fichiers PDB.
    """
    positions_fragments = defaultdict(list)
    
    # Parcourir tous les fichiers PDB dans le dossier de sortie
    for fichier in os.listdir(dossier_fragments):
        if fichier.endswith('.pdb'):
            chemin_fragment = os.path.join(dossier_fragments, fichier)
            try:
                debut, fin = extraire_positions_de_fragment(chemin_fragment)
                # Utiliser le nom du fichier (sans l'extension) comme identifiant de fragment
                nom_fragment = os.path.splitext(fichier)[0]
                # Extraire le nom de la protéine (avant le premier underscore)
                proteine = nom_fragment.split('_', 1)[1] if '_' in nom_fragment else nom_fragment
                
                positions_fragments[proteine].append((nom_fragment, debut, fin))
            except Exception as e:
                print(f"Erreur lors du traitement de {fichier}: {e}")
    
    return positions_fragments

def filtrer_fragments_courts(positions_fragments, longueur_max=500):
    """
    Filtre les protéines pour ne garder que celles dont les domaines sont 
    inférieurs ou égaux à la longueur maximale.
    """
    fragments_filtres = {}
    for proteine, fragments in positions_fragments.items():
        # Calculer la longueur du domaine
        domaines_courts = [
            (fragment, debut, fin) for fragment, debut, fin in fragments 
            if (fin - debut + 1) <= longueur_max
        ]
        
        # Ne conserver que les protéines avec des domaines courts
        if domaines_courts:
            fragments_filtres[proteine] = domaines_courts
    
    return fragments_filtres

def ecrire_positions_fragments(positions_fragments, fichier_sortie):
    """
    Écrit les positions des fragments dans un fichier CSV.
    """
    with open(fichier_sortie, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(["Protéine", "Fragment", "Début", "Fin"])  # En-tête
        for proteine, fragments in positions_fragments.items():
            for fragment, debut, fin in fragments:
                writer.writerow([proteine, fragment, debut, fin])
    print(f"Positions des fragments enregistrées dans {fichier_sortie}")

def construire_graphique_domaine(positions_fragments):
    """
    Construit un graphique montrant les positions des domaines pour chaque protéine.
    """
    fig, ax = plt.subplots(figsize=(20, 15))  # Taille de la figure augmentée pour plus de lisibilité

    # Tracer les fragments pour chaque protéine
    for i, (proteine, fragments) in enumerate(positions_fragments.items()):
        for fragment, position_debut, position_fin in fragments:
            ax.plot([position_debut, position_fin], [i, i], marker='|', 
                    color='skyblue', linewidth=4, 
                    label=proteine if fragment == fragments[0][0] else "")

    # Personnalisation des ticks sur l'axe Y
    ax.set_yticks(range(len(positions_fragments)))
    ax.set_yticklabels(positions_fragments.keys(), fontsize=10)
    ax.set_xlabel("Position dans la séquence protéique", fontsize=12)
    ax.set_ylabel("Protéine", fontsize=12)
    ax.set_title("Positions des domaines alignés pour chaque protéine (≤ 500 aa)", fontsize=14)

    # Amélioration de la légende
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), 
              loc="center left", fontsize=7, bbox_to_anchor=(1, 0.5))

    plt.tight_layout(rect=[0, 0, 0.9, 1])  # Ajuster les marges pour laisser de la place à la légende
    plt.show()

def main():
    # Dossier contenant les fichiers PDB nettoyés
    dossier_fragments = r'C:\Users\Liman\.vscode\Enter\fragments_nettoyés'
    fichier_sortie = "positions_fragments.txt"

    # Obtenir les positions des fragments
    positions_fragments = obtenir_positions_fragments(dossier_fragments)

    # Filtrer les fragments pour ne garder que ceux ≤ 500 aa
    positions_fragments_filtrees = filtrer_fragments_courts(positions_fragments)

    # Sauvegarder les positions dans un fichier texte
    ecrire_positions_fragments(positions_fragments_filtrees, fichier_sortie)

    # Construire le graphique
    construire_graphique_domaine(positions_fragments_filtrees)

if __name__ == "__main__":
    main()