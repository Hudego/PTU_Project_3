import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def lire_positions_fragments(fichier_entree):
    """
    Lit le fichier de positions des fragments et retourne une liste de tous les domaines.
    """
    domaines = []
    
    with open(fichier_entree, 'r') as csvfile:
        # Ignorer l'en-tête
        next(csvfile)
        
        lecteur_csv = csv.reader(csvfile, delimiter='\t')
        for ligne in lecteur_csv:
            proteine, fragment, debut, fin = ligne
            debut = int(debut)
            fin = int(fin)
            domaines.append({
                'proteine': proteine,
                'fragment': fragment,
                'debut': debut,
                'fin': fin,
                'taille': fin - debut + 1
            })
    
    return domaines

def calculer_statistiques_generales(domaines):
    """
    Calcule les statistiques générales sur l'ensemble des domaines.
    """
    # Extraire les données pour les calculs
    tailles = [domaine['taille'] for domaine in domaines]
    debuts = [domaine['debut'] for domaine in domaines]
    fins = [domaine['fin'] for domaine in domaines]

    # Calculer les chevauchements de domaines
    chevauchements = calculer_chevauchements(domaines)

    # Calculs statistiques
    statistiques = {
        'Nombre total de domaines': len(domaines),
        
        # Statistiques de taille des domaines
        'Taille moyenne des domaines': np.mean(tailles),
        'Taille médiane des domaines': np.median(tailles),
        'Écart-type des tailles': np.std(tailles),
        'Taille minimale des domaines': np.min(tailles),
        'Taille maximale des domaines': np.max(tailles),
        
        # Statistiques de position de début
        'Position moyenne de début des domaines': np.mean(debuts),
        'Position médiane de début des domaines': np.median(debuts),
        'Écart-type des positions de début': np.std(debuts),
        'Position minimale de début': np.min(debuts),
        'Position maximale de début': np.max(debuts),
        
        # Statistiques de position de fin
        'Position moyenne de fin des domaines': np.mean(fins),
        'Position médiane de fin des domaines': np.median(fins),
        'Écart-type des positions de fin': np.std(fins),
        'Position minimale de fin': np.min(fins),
        'Position maximale de fin': np.max(fins),
        
        # Informations sur les chevauchements de domaines
        'Nombre de domaines se chevauchant': len(chevauchements),
        'Pourcentage de domaines se chevauchant': (len(chevauchements) / len(domaines)) * 100 if domaines else 0
    }

    return statistiques, chevauchements

def calculer_chevauchements(domaines):
    """
    Calcule les domaines qui se chevauchent.
    """
    chevauchements = []
    
    # Trier les domaines par début
    domaines_tries = sorted(domaines, key=lambda x: x['debut'])
    
    for i in range(len(domaines_tries)):
        for j in range(i+1, len(domaines_tries)):
            # Vérifier s'il y a un chevauchement
            if (domaines_tries[i]['debut'] <= domaines_tries[j]['fin'] and 
                domaines_tries[j]['debut'] <= domaines_tries[i]['fin']):
                chevauchements.append({
                    'domaine1': f"{domaines_tries[i]['proteine']}_{domaines_tries[i]['fragment']}",
                    'domaine2': f"{domaines_tries[j]['proteine']}_{domaines_tries[j]['fragment']}",
                    'debut1': domaines_tries[i]['debut'],
                    'fin1': domaines_tries[i]['fin'],
                    'debut2': domaines_tries[j]['debut'],
                    'fin2': domaines_tries[j]['fin']
                })
    
    return chevauchements

def visualiser_distributions_et_limites(domaines, chevauchements):
    """
    Crée des visualisations avancées des distributions et des limites de domaines.
    """
    tailles = [domaine['taille'] for domaine in domaines]
    debuts = [domaine['debut'] for domaine in domaines]
    fins = [domaine['fin'] for domaine in domaines]

    # Configuration des sous-graphiques
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Analyse approfondie des caractéristiques des domaines')

    # Histogramme des tailles avec courbe de densité
    axs[0, 0].hist(tailles, bins=20, density=True, alpha=0.7, edgecolor='black')
    axs[0, 0].set_title('Distribution des tailles de domaines')
    axs[0, 0].set_xlabel('Taille (acides aminés)')
    axs[0, 0].set_ylabel('Densité')

    # Diagramme de dispersion : début vs fin
    axs[0, 1].scatter(debuts, fins, alpha=0.6)
    axs[0, 1].set_title('Positions de début vs fin des domaines')
    axs[0, 1].set_xlabel('Position de début (acides aminés)')
    axs[0, 1].set_ylabel('Position de fin (acides aminés)')
    axs[0, 1].plot([min(debuts), max(debuts)], [min(debuts), max(debuts)], 'r--', label='Ligne y=x')
    axs[0, 1].legend()

    # Visualisation des chevauchements
    if chevauchements:
        chevauchement_debuts = [c['debut1'] for c in chevauchements] + [c['debut2'] for c in chevauchements]
        chevauchement_fins = [c['fin1'] for c in chevauchements] + [c['fin2'] for c in chevauchements]
        
        axs[1, 0].scatter(chevauchement_debuts, chevauchement_fins, color='red', alpha=0.6)
        axs[1, 0].set_title('Positions des domaines se chevauchant')
        axs[1, 0].set_xlabel('Position de début (acides aminés)')
        axs[1, 0].set_ylabel('Position de fin (acides aminés)')
    else:
        axs[1, 0].text(0.5, 0.5, 'Aucun chevauchement détecté', 
                       horizontalalignment='center', verticalalignment='center')
        axs[1, 0].set_title('Chevauchements de domaines')

    # Distribution des écarts entre début et fin
    ecarts = [domaine['fin'] - domaine['debut'] for domaine in domaines]
    axs[1, 1].hist(ecarts, bins=20, edgecolor='black')
    axs[1, 1].set_title('Distribution des écarts entre début et fin')
    axs[1, 1].set_xlabel('Écart (acides aminés)')
    axs[1, 1].set_ylabel('Fréquence')

    plt.tight_layout()
    plt.show()

def generer_rapport(fichier_entree):
    """
    Génère un rapport complet des statistiques de domaines.
    """
    # Lire les fragments
    domaines = lire_positions_fragments(fichier_entree)
    
    # Calculer les statistiques générales et trouver les chevauchements
    statistiques, chevauchements = calculer_statistiques_generales(domaines)
    
    # Afficher le rapport
    print("=== STATISTIQUES GÉNÉRALES DES DOMAINES ===")
    for cle, valeur in statistiques.items():
        print(f"{cle}: {valeur:.2f}")
    
    # Afficher les détails des chevauchements
    if chevauchements:
        print("\n=== CHEVAUCHEMENTS DE DOMAINES ===")
        for chevauchement in chevauchements:
            print(f"Domaine 1: {chevauchement['domaine1']} (début: {chevauchement['debut1']}, fin: {chevauchement['fin1']})")
            print(f"Domaine 2: {chevauchement['domaine2']} (début: {chevauchement['debut2']}, fin: {chevauchement['fin2']})")
            print("---")
    
    # Visualiser les distributions et limites
    visualiser_distributions_et_limites(domaines, chevauchements)

def main():
    # Chemin vers le fichier de positions des fragments
    fichier_entree = "positions_fragments.txt"
    
    # Générer le rapport
    generer_rapport(fichier_entree)

if __name__ == "__main__":
    main()