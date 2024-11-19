# PTU_Project_3

Bloc 1 : Prise en main et calcul du nombre moyen de repeats WD par protéines.

Objectif : Estimer le nombre moyen de repeats WD par protéine dans les données disponibles pour déterminer combien de repeats forment un domaine WD.

Méthode : 

-Utilisation des données UniProt pour récupérer le nombre total de repeats WD.

-Extraction des informations importantes dans le fichier Excel.

-Identification rapide des protéines à retirer pour le calcul (Protéines trop grosses, nombre incohérent de repeats, …)

-Utilisation de pandas et écriture d’un script python pour manipuler les données du fichier Excel WD_extracted_data.xlsx et filtrer les protéines en fonction de certains critères. Ainsi, on retire les protéines trop grosses avec 3000 acides aminés et on ne garde uniquement les protéines qui ont entre 4 et 8 repeats WD.

-Calculer une première moyenne ne prenant pas en compte les protéines avec plusieurs domaines.

Script Python (3.12.7) :
![image](https://github.com/user-attachments/assets/2b0bf226-25ef-48ac-89b8-042906d6d100)
![image](https://github.com/user-attachments/assets/215bfe0c-a777-4c4c-b92a-9daef99e60f8)

Remarque :Pour exécuter le programme, le fichier Excel et le script doivent se trouver dans le même dossier. J'ai utilisé Visual Studio Code (version 1.95.1) pour exécuter mon script Python.

Résultats observés :
 Avec ce script, on trie un certain nombre de protéines qu’on enlève pour calculer la moyenne. On obtient alors une moyenne de 7 repeats par domaine WD en ayant filtré au total 66 protéines.
 
Conclusion : La moyenne obtenu est assez cohérente car on s’attendait à un nombre de blade entre 4 et 8 environs. Néanmoins, certains problèmes sont assez évidents. Déjà, ce script ne prend pas en compte les protéines qui ont plusieurs domaines WD (ce qui multiplie donc le nombre de repeats sans pour autant que ce soit une erreur). Par la suite, il faudrait identifier manuellement les multi-domaines et faire une moyenne non pas sur le nombre de protéines, mais sur le nombre total de domaines pour avoir une estimation bien plus juste et précise.

Je n’ai également pas réussi à afficher le résultat dans des colonnes différentes pour le fichier csv. Ainsi, je resterais sur un format Excel pour le prochain script pour éviter d’avoir des problèmes de conversions.

Personne ayant travaillé sur le bloc : Hugo Mutschler, 20-21 octobre 2024



Bloc 2 : Identification des protéines avec plusieurs domaines WD et affinage de la moyenne.

Objectif : Identifier les protéines possédant plusieurs domaines WD pour ajuster le calcul de la moyenne et faire un script plus cohérent. Par la suite, l’objectif est de déterminer le nombre de de domaines WD par protéines en utilisant cette moyenne.

Méthode :

-Visualisation des protéines mal annotés en utilisant le schéma des 280 protéines (WD_map.png).

-Visualisation des structures 3D de certaines protéines via AlphaFold pour vérifier le nombre de domaine WD. On cherche le nombre de structures en forme de « donuts ». On vérifie les protéines qui semblent mal annotées avec seulement 1,2 ou 3 repeats et celles qui semblent avoir plusieurs domaines (+ de 8 repeats)

-Création d’une liste de protéines à plusieurs domaines en fonction des annotations UniProt et de la visualisation des structures. Pour gagner du temps, on part du principe que les mêmes familles de protéines ont le même nombre de domaines, ce qui est très souvent le cas.

-Recherche bibliographique pour avoir une idée plus précise du résultat attendu sur le nombre de repeats par domaine.

-Création d’un nouveau script Python plus cohérent, et qui prend en compte les protéines de notre liste avec plusieurs domaines WD. Le script renverra un fichier avec chaque protéine, leurs nombres de domaines, et leurs nombre moyen de repeatWD.

Liste des protéines avec plusieurs domaines (visualisation AlphaFold):

-EMAL5,6 = 6 domaines (x2) -APAF = 2 domaines  -CFA = 2 domaines (x4) -TEP1 = 3 domaines -STB5L = 2 domaines -STXB5 = 2 domaines -CF251 = 2 domaines -L2GL = 2 domaines (x2) -PWP2 = 2 domaines -ELP2 = 2 domaines 39 -UTP4 = 2 domaines -NWD1 = 2 domaines -EMAL2,1 = 2 domaines (x2) -TBL3 = 2 domaines -GEMI5 = 2 domaines -MABP1 = 2 domaines -WDR90 = 4 domaines -WDR6 = 3 domaines -WDR3 = 2 domaines -WDR36 = 2 domaines -WDR64 = 2 domaines -WDR62 = 2 domaines -WDR27 = 2 domaines -WDR11 = 2 domaines -DMX = pas présent dans le fichier Excel et pas prédite par AlphaFold.

On observe que la plupart des protéines à plusieurs domaines ont 2 domaines. On observe également la protéine EMAL5 et EMAL6 qui sont assez différentes des autres avec un total de 6 domaines WD dans leurs structures.

On peut refaire une moyenne en prenant en compte les protéines avec plusieurs domaines WD :

D’après les annotations UniProt et le fichier Excel, on a : 2131 WD

On a au total 280 protéines dont 24 protéines qui ont plus que 1 domaines, ce qui fait 280-24 protéines avec 1 domaine, soit 256 protéines avec 1 domaines.

Si on rajoute les protéines qui ont plusieurs domaines, ça fait 72 domaines + 256 domaines = 328 domaines pour nos 280 protéines.

On fait la moyenne pour obtenir le nombre de repeatWD par domaine : 2131 / 328 = ~ 6,5 repeats par domaines WD.

Recherche bibliographique : 

Les bêta-propeller les plus communs contiennent généralement 7 ou 8 pales. 

Source: Jain BP, Pandey S. WD40 Repeat Proteins: Signalling Scaffold with Diverse Functions. Protein J. 2018 Oct;37(5):391-406. doi: 10.1007/s10930-018-9785-7. PMID: 30069656.

Remarques supplémentaires :

Après vérification sur plusieurs protéines en utilisant AlphaFold, il semblerait que les protéines qui ont une annotation avec des oublis de repeats ne contiennent à chaque fois qu’un seul domaine. On va ainsi faire un script avec les règles suivantes :

-Toutes les protéines ont 1 domaines, sauf celles qu’on a vérifié manuellement. 

-On demande au script de nous faire un fichier Excel avec sur 1 colonne le nom des protéines, sur 1 colonne le nombre de domaines, et sur 1 colonne le nombre de repeats.

-On utilise une moyenne de 7 repeats par domaine pour faciliter les calculs et pour prendre un résultat se trouvant entre la bibliographie et proche de ce qu’on a trouvé en calculant la moyenne.

-On retire les protéines DMX car elles ne sont pas prédites par AlphaFold et sont absente du fichier Excel


Script Python (3.12.7) :

![image](https://github.com/user-attachments/assets/df5760b9-186e-4f6d-b2a8-29ad7dc8482c)

Remarques : Le fichier Excel obtenu est visible dans le dossier sous le nom « Domaines_WD_par_protéines »

Conclusion :

Ce script nous donne un fichier Excel avec chaque protéine, leurs nombres de domaines, et leurs nombres de repeats moyens. Il est possible de vérifier chaque protéine avec AlphaFold, et le résultat est très souvent correct ou très proche de la réalité.

Une moyenne se situant entre 6,5 et 7 repeats par domaine semble donc être juste et utilisable pour la suite de nos opérations.


Personne ayant travaillé sur le bloc : Hugo Mutschler, 28-31 octobre 2024



Bloc 3: Création d’une librairie de fragments de protéines humaines ayant un domaine WD

Objectif: Récupérer la structure prédites alphafold de protéines ayant un domaine WD et les fragmenter en fonction de leur score PLDDT.

Méthode:

●	Utilisation des id PDB de chaque protéine pour les prédire avec AlphaFold.
●	Automatisation du processus de prédiction des protéines présentes dans un fichier Excel.
●	Lecture des fichiers PDB des structures prédites et analyse des scores de PLDDT (colonne B-Factor).
●	Fragmentation des structures en fonction du score PLDDT.
●	Création de fichier individuels pour chaque structure/fragment obtenu

Script Python pour l’automatisation  (3.12.2)
![Fragments 11](https://github.com/user-attachments/assets/0baa9b78-2e64-4ebe-834f-0cbea5e472e8)
![fragment22](https://github.com/user-attachments/assets/6502bd81-e68b-424e-9f7a-3d75920f37e4)


Le programme nous permet d’avoir les fragments de chaque protéine, un total de 2551 fragments est observé pour 280 protéines.

Conclusion: 

Le programme nous permet de fragmenter les protéines, mais nécessite encore une étape de vérification de la qualité des fragments générés. 

Personne ayant travaillé sur le bloc : Aiman Limani, Ismail Unlu ; 20-22 octobre


Bloc 4 : Superposition des fragments obtenus sur un model de beta-propeller a fin de verifier l'annotation Uniprot .
Objectif: Superposer les fragments obtenus des structures prédites par rapport à un modèle de beta-propeller afin de retrouver le nombre moyen de WD repeat des protéines humaines.
Méthode:
●	Choix d’un modèle de beta-propeller a 7 blades ( moyenne obtenue par l’annotation de Hugo). Id beta-propeller
●	utilisation  de conda (24.1.2)
conda create -n pymol-env python=3.8 
conda activate pymol-env
conda install -c schrodinger pymol
cd C:\Users\Liman\.vscode\Enter
python "superposition fragments-Modele.py"
conda install matplotlib

●	script python  pour automatiser les superposition des fragments au modèle par PyMol
●	Analyse et mesure du nombre de fragments superposé ayant un bon score RMSD pour chaque protéine, un score RMSD faible signifié une bonne similarité et superposition
●	affichage d’un graphique nous donnant le nombre de fragments bien aligné par protéine

Script Python pour l’automatisation  (3.12.2)
![Fragments1](https://github.com/user-attachments/assets/4aa216b7-ee49-4119-8260-aa82bb46e4ff)
![Fragments2](https://github.com/user-attachments/assets/786f3b9d-30e1-406a-86fc-358270ca7225)



Résultats observés:

résultats des superpositions trop imparfait et inutilisables ( ex: des protéines avec 1 ou 2 fragments aligné et certaines à 50 fragments aligné)


Conclusion:

En superposant les fragments créés avec le beta-propeller et en gardant seulement ceux avec un score RMSD faible on pense garder que les partie/fragments qui correspondent au beta-propeller.

Cependant  les résultats restent trop aberrants et pas utilisables, le code nécessite des améliorations ou une autre approche est à tester, nous avons utilisé un base de 280 protéines qui peuvent avoir un ou plusieur domaine WD c’est pour cela qu’il faut réaliser à nouveau un test avec les 256 proteines isolé par hugo qui possèdent un seul domaine pour permettant d’avoir une distribution plus équitable et nous permettant de mieux comparer les protéines entre elles et leurs fragments.

Personne ayant travaillé sur le bloc: Aiman Limani, 1-5 novembre

Bloc 5-6 Alignez les séquences avec ces nouvelles limites pour tenter de mieux redéfinir les repeats WD et Proposer de nouvelles annotations prenant en compte l’alignement de séquence et de structure:
Objectif: Redéfinir les repeats WD et proposer des annotations mises à jour.

Méthode:

Nous devons d’abord préparer les séquences correspondant aux nouvelles limites des repeats WD et les compiler dans un fichier fasta.

Pour cela nous allons utiliser Jalview et l’outil MAFFT plus précisément car il gère des séquences divergentes ou contenant des motifs répétitifs, comme les repeats WD.

A la suite de l'alignement des séquences nous devons analyser les résultats obtenus, pour cela nous devons activer la coloration par conservation pour identifier les motifs conserver. Pour cette tâche nous devons regarder sur les différentes séquences afin de trouver des motifs qui correspondent à des éléments spécifiques des repeat WD.

Ensuite, le logiciel Jalview nous permet d’ajouter de nouvelle annotation en effet, Après superposition de structures et l’alignement de séquences le but est de trouver de nouvelles annotations afin de montrer les nouveaux motifs.

Finalement nous devons comparer les séquences de bases avec nos nouvelles séquences afin d’en tirer les conclusions.

Ismail Unlu



