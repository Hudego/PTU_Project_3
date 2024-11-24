# PTU_Project_3

## **Bloc 1 : Prise en main et calcul du nombre moyen de repeats WD par protéines**

**Objectif :**  
Estimer le nombre moyen de repeats WD par protéine dans les données disponibles pour déterminer combien de repeats forment un domaine WD.

**Méthode :**  
- Utilisation des données UniProt pour récupérer le nombre total de repeats WD.  
- Extraction des informations importantes dans le fichier Excel.  
- Identification rapide des protéines à retirer pour le calcul (protéines trop grosses, nombre incohérent de repeats, etc.).  
- Utilisation de pandas et écriture d’un script Python pour manipuler les données du fichier Excel *WD_extracted_data.xlsx* et filtrer les protéines en fonction de certains critères. Ainsi, on retire les protéines trop grosses (plus de 3000 acides aminés) et on ne garde que les protéines ayant entre 4 et 8 repeats WD.  
- Calculer une première moyenne sans prendre en compte les protéines avec plusieurs domaines.  

**Script Python (3.12.7) :**  
![image](https://github.com/user-attachments/assets/2b0bf226-25ef-48ac-89b8-042906d6d100)  
![image](https://github.com/user-attachments/assets/215bfe0c-a777-4c4c-b92a-9daef99e60f8)  

**Remarque :**  
Pour exécuter le programme, le fichier Excel et le script doivent se trouver dans le même dossier. J'ai utilisé Visual Studio Code (version 1.95.1) pour exécuter mon script Python.

On utilise le module pandas (version 2.2.3). Ce module sert à manipuler, analyser et transformer facilement des données.

**Résultats observés :**  
Avec ce script, nous avons trié un certain nombre de protéines que nous avons retirées pour calculer la moyenne. On obtient alors une moyenne de **7 repeats** par domaine WD, après avoir filtré un total de 66 protéines.  

**Conclusion :**  
La moyenne obtenue est cohérente car on s’attendait à un nombre de blades entre 4 et 8. Cependant, ce script ne prend pas en compte les protéines ayant plusieurs domaines WD (ce qui multiplie le nombre de repeats sans que ce soit une erreur). Par la suite, il faudra identifier manuellement les multi-domaines et calculer une moyenne basée sur le nombre total de domaines pour une estimation plus précise.  

Je n’ai pas réussi à afficher le résultat dans des colonnes distinctes pour le fichier CSV. Par conséquent, je resterai sur un format Excel pour le prochain script pour éviter les problèmes de conversion.

**Personne ayant travaillé sur le bloc :** Hugo Mutschler, 20-21 octobre 2024  

---

## **Bloc 2 : Identification des protéines avec plusieurs domaines WD et affinage de la moyenne**

**Objectif :**  
Identifier les protéines possédant plusieurs domaines WD pour ajuster le calcul de la moyenne et produire un script plus cohérent. Par la suite, l’objectif est de déterminer le nombre de domaines WD par protéines en utilisant cette moyenne.

**Méthode :**  
- Visualisation des protéines mal annotées à l'aide du schéma des 280 protéines (*WD_map.png*).  
- Visualisation des structures 3D de certaines protéines via AlphaFold pour vérifier le nombre de domaines WD (observation des structures en forme de "donuts"). Vérification des protéines semblant mal annotées avec moins de 7 repeats et de celles ayant plusieurs domaines (+ de 8 repeats).  
- Création d’une liste de protéines à plusieurs domaines basée sur les annotations UniProt et la visualisation des structures. Par souci d'efficacité, nous supposons que les familles de protéines similaires ont le même nombre de domaines.
- Recherche bibliographique pour affiner le résultat attendu concernant le nombre de repeats par domaine.  
- Création d’un nouveau script Python prenant en compte les protéines avec plusieurs domaines WD. Le script génère un fichier contenant le nom des protéines, leur nombre de domaines, et leur nombre moyen de repeats WD.  

**Liste des protéines mal annotés avec des oublis de repeats (Visualisation WD_map.png):**
- **BCAS3**
- WDR93
- VPS8
- **NBEL1**
- WDCP
- DC4L2
- DCAF4
- FRITZ
- RIC1
- NBAS
- **AMRA1**
- RFWD3
- **PAN2**
- DNAI3
- DC211
- DCAF1
- **TLE7**
- DC211
- DCAF1
- TLE7
- DC212
- WDFY3
- NBEA

En vérifiant manuellement (visualisation alphafold), on se rend compte que la plupart des protéines mal annotés de cette liste sont composé d'un seul domaine avec 7 repeats. Les protéines listés en **gras** ont été vérifié manuellement et contiennent bien 7 repeats.

Ces informations seront utilisés lors du prochain script pour faire une moyenne d'avantage correct.



**Liste des protéines avec plusieurs domaines (visualisation AlphaFold) :**  
- EMAL5, EMAL6 : 6 domaines (x2)  
- APAF : 2 domaines  
- CFA : 2 domaines (x4)  
- TEP1 : 3 domaines  
- STB5L : 2 domaines  
- STXB5 : 2 domaines  
- CF251 : 2 domaines  
- L2GL : 2 domaines (x2)  
- PWP2 : 2 domaines  
- ELP2 : 2 domaines  
- UTP4 : 2 domaines  
- NWD1 : 2 domaines  
- EMAL2, EMAL1 : 2 domaines (x2)  
- TBL3 : 2 domaines  
- GEMI5 : 2 domaines  
- MABP1 : 2 domaines  
- WDR90 : 4 domaines  
- WDR6 : 3 domaines  
- WDR3 : 2 domaines  
- WDR36 : 2 domaines  
- WDR64 : 2 domaines  
- WDR62 : 2 domaines  
- WDR27 : 2 domaines  
- WDR11 : 2 domaines  

Protéine exclue : **DMX** (absente du fichier Excel et non prédite par AlphaFold).  Cela indique certainement une protéine fragmentée.

**Nouveau calcul de la moyenne :**  
- Données UniProt et fichier Excel : **2131 repeats WD**  
- Total de 280 protéines, dont 24 avec plusieurs domaines, soit :  
  - **256 protéines avec 1 domaine**  
  - **24 protéines représentant 72 domaines**  
- Total : **328 domaines** pour 280 protéines.  

**Moyenne ajustée :**  
2131 repeats WD / 328 domaines ≈ **6,5 repeats par domaine WD**  

**Recherche bibliographique :**  
Les bêta-propellers les plus communs contiennent généralement **7 ou 8 blades**.  
Source : Jain BP, Pandey S. *WD40 Repeat Proteins: Signalling Scaffold with Diverse Functions*. *Protein J.* 2018 Oct;37(5):391-406. doi: 10.1007/s10930-018-9785-7. PMID: 30069656.  


**Nouveau script Python (3.12.7) :**  
![image](https://github.com/user-attachments/assets/df5760b9-186e-4f6d-b2a8-29ad7dc8482c)  

**Conclusion :**  
Ce script génère un fichier Excel contenant chaque protéine, son nombre de domaines, et son nombre moyen de repeats. Une moyenne située entre **6,5 et 7 repeats** par domaine semble juste et utilisable pour les analyses suivantes. Comme notre premier script nous indiquait plutôt une moyenne de 7 repeats et que la recherche bibliographique va dans ce sens également, on décide de partir sur une moyenne finale de **7 repeats par domaine WD.**

**Personne ayant travaillé sur le bloc :** Hugo Mutschler, 28-31 octobre 2024  

---

## **Bloc 3 : Création d’une librairie de fragments de protéines humaines ayant un domaine WD**

**Objectif :**  
Récupérer les structures prédites par AlphaFold des protéines ayant un domaine WD et les fragmenter en fonction de leur score PLDDT.  

**Méthode :**  
- Extraction des identifiants PDB pour chaque protéine et prédiction via AlphaFold.  
- Automatisation de la récupération et de l’analyse des fichiers PDB grâce à un script Python.  
- Analyse des fichiers PDB pour extraire les scores PLDDT (colonne *B-Factor*).  
- Fragmentation des structures en fonction des valeurs de PLDDT pour générer des fragments de haute qualité.  
- Création de fichiers individuels pour chaque fragment généré.

**Script Python utilisé (3.12.7) :**  


**Résultats observés :**  
Le programme a permis de générer un total de **2551 fragments** à partir de 280 protéines. Chaque fragment a été sauvegardé dans un fichier individuel, prêt pour une analyse ultérieure. 

**Informations supplémentaires:**
Pour découper les fragments, on a choisi d'utiliser un seuil (treshold) de 70 pour le score pLDDT (Predicted Local Distance Difference Test). Ce score allant de 0 à 100 évalue la confiance de la prédiction d'alphafold au niveau résiduel. A partir de 70, on estime qu'on a une bonne confiance et que la structure est probable.

L'objectif pour nous est de trouver un score qui permet d'éviter les régions désordonnées (score trop faible) mais garder en compte un certains nombres de régions qui pourraient être exclus si on choisis un seuil trop élevé. (par exemple, un seuil de 90 pourrait exclure des régions qui sont pourtant pertinentes pour nous.)

**Modules Utilisés:**

- **requests** (v2.31.0) : Permet d'effectuer des requêtes HTTP (GET, POST, etc.) pour interagir avec des APIs ou récupérer des données en ligne.
- **pandas** (version 2.2.3). Ce module sert à manipuler, analyser et transformer facilement des données.


**Conclusion :**  
Ce programme fournit une base solide pour l’analyse des fragments de protéines. Cependant, il nécessite une étape supplémentaire pour vérifier la qualité des fragments générés, en particulier pour confirmer leur pertinence par rapport aux domaines WD. 

**Verification des fragments:**

Pour avoir une première évaluation des fragments générés par notre script, nous avons decidé de superposer les 3 premiers fragments générés de notre liste (protéine A0A1W2PR48) avec notre domaine WD de reference (Protéine B2J0I0 et son domaine WD 7bid.)

L'allignement semble correct dans l'ensemble et on observe pour les 3 fragments des valeurs assez faible de RMSD indiquant une bonne superposition.

Screenshot de la superposition realisé avec le logiciel PyMOL (version 3.0.3)
![Alligement entre domaine Wd 7bid et trois fragment](https://github.com/user-attachments/assets/1312043b-51e2-496e-b4fc-659e9499fc76)

-Alignement fragment 1: RMSD 1.399

-Alignement fragment 2: RMSD 2.276

-Alignement fragment 3: RMSD 3.103

**Personnes ayant travaillé sur le bloc :** Aiman Limani, Ismail Unlu (20-22 octobre 2024), modifications faites par Hugo Mutschler pour la verification des fragments (20-21 novembre 2024)

---

## **Bloc 4 : Superposition des fragments sur un modèle de beta-propeller pour vérifier les annotations UniProt**

**Objectif :**  
Superposer les fragments obtenus sur un modèle de beta-propeller afin de confirmer les annotations UniProt et affiner l’estimation du nombre moyen de repeats WD par protéine.  

**Méthode :**  
1. **Préparation des outils :**  
   - Choix d’un modèle de beta-propeller à 7 blades (moyenne obtenue dans le bloc 2). On décide d'utiliser la protéine B2J0I0 et son domaine WD 7bid.
   - Installation et configuration de PyMol avec Conda (version 24.1.2).  
2. **Automatisation de la superposition :**  
   - Écriture d’un script Python pour superposer automatiquement les fragments sur le modèle via PyMol.  
   - Calcul des scores RMSD pour évaluer la qualité de la superposition.  
3. **Analyse des résultats :**  
   - Identification des fragments bien alignés avec un faible RMSD.  
   - Création d’un graphique représentant le nombre de fragments bien superposés par protéine.  

**Script Python utilisé (3.12.7) :**  
  

**Résultats observés :**  
Les résultats des superpositions étaient imparfaits et inutilisables pour l’analyse finale :  
- Certaines protéines avaient seulement 1 ou 2 fragments alignés correctement, tandis que d’autres en avaient jusqu’à 50.  
- Une distribution incohérente des alignements a été observée.
![image](https://github.com/user-attachments/assets/48fe7a86-f467-4096-bda4-005e297c85f7)

On s'interesse ensuite aux fragments qui ont un RMSD faible et un nombre conséquent d'atomes alignés. Pour ce faire, on modifie legerement notre script d'alignement en utilisant matplotlib pour générer un Scatterplot et calculer le RMSD avec Pymol. On utilise le log(RMSD) pour une meilleur visualisation des points. Dans cet exemple, on garde uniquement les fragments avec une longueur minimal de 50 acides aminés.


![Scatterplot aamin=50](https://github.com/user-attachments/assets/1d8bd05f-e7b3-46fe-b39d-6afa184c158d)


**Modules Utilisés:**
- **os** (v3.10) : Gestion des interactions avec le système de fichiers (parcours de dossiers, manipulation de chemins).
- **pymol** (v2.5.0) : API pour utiliser PyMOL, un outil de visualisation et de manipulation de structures moléculaires.
- **matplotlib.pyplot** (v3.8.0) : Création de graphiques et visualisations en Python.
- **collections.defaultdict** (v3.10) : Permet de créer des dictionnaires avec des valeurs par défaut.
- **concurrent.futures.ThreadPoolExecutor** (v3.10) : Parallélisation des tâches pour améliorer les performances.
- **tqdm** (v4.66.1) : Ajout d'une barre de progression pour suivre l'avancement des boucles.

**Conclusion :**  
Bien que l’approche semble prometteuse, les résultats sont trop aberrants pour être exploitables en l’état. Une nouvelle tentative avec un jeu de données plus homogène (les 256 protéines à domaine unique identifiées dans le bloc 2) pourrait améliorer la fiabilité des alignements et permettre une analyse plus pertinente.  

**Personne ayant travaillé sur le bloc :** Aiman Limani (1-5 novembre 2024)  

---

## **Bloc 5-6 : Alignement des séquences et proposition de nouvelles annotations**

**Objectif :**  
Redéfinir les limites des repeats WD à l’aide d’un alignement de séquences et proposer de nouvelles annotations basées sur l’analyse des alignements et des structures.

**Méthode :**  
1. **Préparation des séquences :**  
   - Extraction des séquences correspondant aux nouvelles limites des repeats WD.  
   - Compilation de ces séquences dans un fichier FASTA.  
2. **Alignement des séquences :**  
   - Utilisation de MAFFT pour gérer les séquences divergentes contenant des motifs répétitifs.  
   - Analyse des alignements dans Jalview, avec coloration par conservation pour identifier les motifs conservés spécifiques aux repeats WD.  
3. **Proposition de nouvelles annotations :**  
   - Superposition des structures alignées avec les séquences pour identifier les motifs pertinents.  
   - Ajout de nouvelles annotations à l’aide de Jalview.  
4. **Comparaison des séquences :**  
   - Comparaison des séquences initiales avec les séquences annotées pour évaluer les améliorations apportées.  

**Résultats attendus :**  
L’identification de nouveaux motifs spécifiques aux repeats WD et une mise à jour des annotations existantes pour mieux refléter les données structurelles et séquentielles.  

**Conclusion :**  
Le travail est en cours. L’alignement des séquences et la proposition d’annotations nécessitent une validation supplémentaire pour s’assurer de leur pertinence.  

**Personne ayant travaillé sur le bloc :** Ismail Unlu  


