# PTU_Project_3

**Cahier de laboratoire présenté par**  
*Hugo MUTSCHLER*, *Aiman LIMANI* et *Ismail UNLU*

**Structure du Projet**

Fichiers/ : Contient les fichiers necessaires au projet, à l'utilisation des scripts, ...

Scripts/ : Contient les scripts Python du projet.

Resultats/ : Résultats générés après l'exécution des scripts.

---

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

J'ai eu quelques soucis à afficher les résultats dans des colonnes distinctes pour le fichier CSV. Par conséquent, je resterai sur un format Excel pour le prochain script pour éviter les problèmes de conversion.

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
![image](https://github.com/user-attachments/assets/02398155-75b6-4593-9460-b0901c60f677)

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

**Script Python utilisé (3.12.7) : Fragments_WD.py**  


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

**Amelioration du systeme de fragmentation des proteines predites**

Pour ameliorer la fragmentation et reduire le temps de calcul il a fallu rajouter certaines contraintes au programme, la contrainte principale etant celle du plddt qui ne doit pas etre inferieur à 70, ensuite pour que un fragments puisse etre comptabilisé il lui faut au minimum 9 aa qui se suivent avec un score PLDDT>70, ensuite une marge d"erreur de 5aa est permise pour eviter de couper le fragments a cause de quelques acides aminé negligables, pour eviter de prendre en compte certaines region bien conservé qui peuvent posseder un score superier a 70, nous avons decider de garder des fragments qui ont au minimum 4 aa avec un plddt>90 ( ceci a été decidé apres avoir constaté que dans le domaine WD il y avait une presence de feuillet Beta qui avait un trés grand score).

Pour tester la qualité de l'amelioration on va re-aligner les fragments de la proteine A0A1W2PR48 avec le 7bid, dans un premier temps on a reussi a diminuer le nombre de fragments à 2, et pour des scores de RMSD bien meilleurs:

Screenshot de la superposition realisé avec le logiciel PyMOL (version 3.0.3):
![image](https://github.com/user-attachments/assets/051586c6-24cf-48f3-98ad-d67fec7c27cd)


- Alignement fragment 1: RMSD 0,867

- Alignement fragment 2: RMSD 2.267

**Personnes ayant travaillé sur le bloc :** Aiman Limani, Ismail Unlu (20-22 octobre 2024), modifications faites par Hugo Mutschler pour la verification des fragments (20-21 novembre 2024), Amelioration de la fragmentation des proteines realisé par Aiman LIMANI ( 22-24  novembre 2024).

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

**Script Python utilisé (3.12.7) :Superposition fragments-Modele.py**   
  

**Résultats observés :**  
Les résultats des superpositions étaient imparfaits et et encore améliorable pour l’analyse finale :  
- Certaines protéines avaient seulement 1 ou 2 fragments alignés correctement, tandis que d’autres en avaient jusqu’à 50.  
- Une distribution incohérente des alignements a été observée.
![image](https://github.com/user-attachments/assets/48fe7a86-f467-4096-bda4-005e297c85f7)


**Amelioration de la superposition des fragments au modele**

L'amelioration de la fragmentation des proteines on permis une meilleur superposition generale, pour ameliorer encore mieux la superposition a son tour on a defini un taille minimale du fragment a superposer et augmenter le RMSD a 2,5 ( on pourrait encore l'augmenter d'aventage). Au lieu d'essayer de superposer touts les fragments de maniere parfaite pour toutes les proteines nous avons decider de compter sur la qualité que sur la quantité, pour cela nous avons regroupé les proteines en deux fichier distinct apres superposition, le premier regroupe les proteines qui ont au moins un fragments avec un RMSD <2,5, et un fichier qui regroupe des proteines qui n'ont aucun fragment avec un faible RMSD, cette sepration nous permet donc de travailler de maniere plus specfique et precise, les proteines qui n'ont pas de fragment avec un bon rmsd pourrait etre analysé manuellement.

**Script Python utilisé (3.12.7) :Amelioration superposition.py**  

**Annotation des domaines en fonction des fragments aligné**

Apres avoir superposé les fragments et obtenu un fichier contenant les differents proteines et leurs fragments RMSD<2,5 nous avons pu alors essayer de regarder a quoi correspond le premier et le dernier acide aminé dans le fichier PDB de chaque fragment RMSD<2,5 pour savoir quelle regions ils couvrent sur leur proteine.On a ensuite essayé de contruire un graphique de "couverture de fragments".

Les resulats de l'annotation sont les suivant:
![image](https://github.com/user-attachments/assets/9bb737c9-fffc-4fe6-900e-89b55c09a7e5)

**Resultats:**

On remarque une region hyper representé entre la position N-terminale de la proteine et les position 500aa.
Voir fichier "image_position_1" pour une meilleur visibilité

**Conclusion:**

Apres avoir superposé et annoté les fragments aligné sur les sequences de leurs proteines on peut eventuellement supposé que le domaine WD se situe generalemnt dans la region N-Ter des proteines, cependant l'analyse n'est pas exhaustive et necessite des amelioration comme tenir en compte de la taille de chauqe proteine differement.


On s'interesse ensuite aux fragments qui ont un RMSD faible et un nombre conséquent d'atomes alignés. Pour ce faire, on modifie legerement notre script d'alignement en utilisant matplotlib pour générer un Scatterplot et calculer le RMSD avec Pymol. On utilise le log(RMSD) pour une meilleur visualisation des points. Dans cet exemple, on garde uniquement les fragments avec une longueur minimal de 50 acides aminés.


![Scatterplot aamin=50](https://github.com/user-attachments/assets/1d8bd05f-e7b3-46fe-b39d-6afa184c158d)

**Observations:**

En bas à droite, on observe tout les fragments qui se sont mal alignés. En théorie, on devrait observer une zone en haut au miieu qui correspond aux fragments avec une bonne superposition qui devraient donc en théorie contenir les domaines WD (superposition avec notre domaine de reference). Cela devrait nous permettre d'identifier les fragments de chaque protéines contenant le domaine WD.

Ici, on observe que la frontière n'est pas clairement définie. Pour ce faire, on va revenir en arrière et essayer de modifier les paramètres du découpage des fragments pour avoir une moins grosse fragmentation.
Nous allons essayer d'utiliser les paramètres suivants:

-Gap de 20 acide aminés max. (En utilisant un gap de 30 acides aminés, il n'y a plus trop de fragmentation donc on prefere rester à 20).

-pLDDT de 70 (deja le cas actuellement).

-Supprimer les fragments de moins de 30aa de longs, ce qui ne suffit même pas pour un blade.

-Rajouter quelques protéines n'ayant pas de domaines WD pour avoir une meilleur visualisation de la frontière. (~100 protéines)

![Scatterplot 30aa gap + random prot](https://github.com/user-attachments/assets/fa11f148-9f3e-4570-bb32-4e8249b6e8ea)


**Observations:**

En modifiant quelques paramètres pour la fragmentaion et en rajoutant une centaine de protéines supplémentaires n'ayant pas de domaines WD, on obtient un graphique deja plus pertinent avec une séparation plus distincte. A présent, on va devoir identifier quels point correspondent à des superpostiions utilisables et pertinentes. Il faut définir la limite en regardant manuellement assez grossièrement et identifier la liste de fragments qui se superposent bien à notre domaine de référence.

**Modification des paramètres de fragmentations:**

-En utilisant un gap de 30 acide aminés pour la fragmentation, on obtient: **467 fragments**

-En utilisant un gap de 20 acide aminés pour la fragmentation, on obtient: **547 fragments**

-En utilsant un gap de 20 acides aminés et en ajoutant des protéines externes qui n'ont pas de domaines WD, on se retrouve au final avec: **641 fragments**. C'est cette methode qu'on a utilisé pour générer notre Scatterplot.

**Fragments conformes aux critères (log(RMSD) < 1 et >= 400 atomes alignés) :**

![Limiation](https://github.com/user-attachments/assets/6e2f6a8c-ea69-40a6-8028-02050f36a836)


Pour définir la limite des fragments utilisable, nous avons regardés manuellement en superposant plusieurs fragments avec Pymol pour voir jusqu'ou les résultats étaient pertinent. Cette "frontière" pourrait encore être amélioré en utilisant un moyen plus automatique.
  
On se retrouve donc avec **248 fragments** dans cette liste, retrouvable dans les dossiers "fragments conformes".

Attention, les protéines contenant plusieurs domaines WD n'ont pas été prise en compte car Pymol va superposer uniquement un seul domaine sur les deux, et donc obtenir un mauvais RMSD. Comme il s'agit de cas particuliers et qu'ils sont assez compliqué à gérer, on décide de ne pas les prendres en compte pour la suite.

**Modules Utilisés:**
- **os** (v3.10) : Gestion des interactions avec le système de fichiers (parcours de dossiers, manipulation de chemins).
- **pymol** (v2.5.0) : API pour utiliser PyMOL, un outil de visualisation et de manipulation de structures moléculaires.
- **matplotlib.pyplot** (v3.8.0) : Création de graphiques et visualisations en Python.
- **collections.defaultdict** (v3.10) : Permet de créer des dictionnaires avec des valeurs par défaut.
- **concurrent.futures.ThreadPoolExecutor** (v3.10) : Parallélisation des tâches pour améliorer les performances.
- **tqdm** (v4.66.1) : Ajout d'une barre de progression pour suivre l'avancement des boucles.



**Superposition de nos fragments conformes à notre domaine de reference.**

![image](https://github.com/user-attachments/assets/f1d55104-44fa-4e1e-a97b-f688b57d71b4)


L'image complete est accessible dans nos dossiers.


**Conclusion :**  
A faire

**Personne ayant travaillé sur le bloc :** Aiman Limani (1-5 novembre 2024), Hugo Mutschler (22-25 novembre 2024), Amelioration de la superposition et positionnement des domaines sur les sequences proteiques( pas toutes) par Aiman LIMANI ( 22-24 Novembre 2024)

---
## **Bloc 5 : Annotation des domaines complets predis par Alphafold **

A fin d'avoir un meilleur appercu est de meilleurs resultats une autre approche serait d'isoler directement le domaine WD entier de chaque proteine, ceci va nous eviter des erreurs comme la technique de fragmentation par PLDDT qui incorpore des regions non structuré indesiré. Le but principal est de telechargé toutes les proteines presentes dans le fichier excel, a l'aide de leur id uniprot alpha fold predis leurs strcuture individuelle, ensuite on va effectuer directement une superposition des strcutures predites sur le modele de WD domain 7bid, on va ensuite calculer la distance de touts les atome set supprimer tout ceux qui ont une distance superieur a 5 A° du modele, ceci va nous permettre d'avoir un WD domain nottoyé et complet.

Le code python pour réalisé cette tache est le "Fragmentation_WD_domains_complets.py"

Apres avoir obtenu des fragments des proteines contenat seulement les domains WD complets pour chaque proteine on va essayer de trouver leur position dans la sequence des proteines a fin de comprendre la ou les domaines sont situé.

Le code python pour réalisé cette tache est le "Positionnement_des_domaines_2.py"

Le positionnement des domaines nous permet d'obtenir plusieurs information tels que la position moyenne de l'acide aminé initial/final, la taille et la correlation (position debut/fin)

Le code python pour réalisé cette tache est le "statistiques_domaines.py"

![image](https://github.com/user-attachments/assets/0eff3169-a223-4cf3-b28a-91112ab54cbb)

Une fois que nous avons obtenu et analysé les differents domaines WD, nous allons ensuite essayer d'aligner l'ensemble des sequences proteiques a fin de relever les differentes regoins ou motifs conservé entre domaines. Nous allons dans un premier cas transformer les fichiers pdb en fichiers fasta, ces fichiers vont etre concatené pour etre utilisé avec MAFFT afin de realiser un alignement multiple. L'affichage de l'alignement sera fait sur Jalview.

Dans un premier temps nous alons transformer les fichier PDB des differents domaines predis en fichier fasta.

Le code python pour réalisé cette tache est  "pdb_fasta.py"

Une fois le fichier fasta pour chaque proteine obtenu il va falloir concatener et reunier toutes les sequences dans un seul et meme fichier, ce fichier va etre ensuite donnée a MAFFT Online, l'utilisation du site MAFFT permet une meilleur familiarisation et est plus intuitif. Une fois le fichier avec les sequences concatené est televersé dans MAFFT nous allons avoir plusier resultats, il va faloir telechargé le fichier d'alignement pour le visualiser sur Jalview.

Le code python pour réalisé cette tache est  "alignement.py"

Une fois sur Jalview nous pouvons analyser l'alignement dans le quel on remarque plusieurs points interessants:

![image](https://github.com/user-attachments/assets/98c9e252-2a4e-4d8c-88aa-56751fd73885)

Nous pouvons voir sur l'ensemble de la sequence d'alignement plusieurs position ou la conservation des aa est tres fortes, les aa tres bien conservé sont les W et D qui des fois ont 90% de conservation

**Personne ayant travaillé sur le bloc :** Aiman LIMANI


## **Bloc  : Alignement des séquences**

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
Nous avons discuté avec le groupe 5, qui travaille également sur les repeats WD, et avons pu comparer certains de nos résultats avec les leurs. Ils avaient déjà tenté de réaliser un alignement de séquences, mais les résultats se sont avérés peu pertinents, et les alignements multiples étaient très difficiles à analyser. Par conséquent, nous avons décidé d’abandonner l’idée d’effectuer des alignements pour nous concentrer davantage sur les étapes de fragmentation et de superposition (blocs 3 et 4).

**Personne ayant travaillé sur le bloc :** Ismail Unlu  


