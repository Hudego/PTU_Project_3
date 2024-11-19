import pandas as pd

# Chargement des données
length_data = pd.read_excel('WD_extracted_data.xlsx', sheet_name='protein_length')
data = pd.read_excel('WD_extracted_data.xlsx')

# On filtre les repeats WD et les données qui nous intéressent
wd_data = data[data['feature'].str.contains('WD', case=False) | (data['feature'] == 'WD repeat-containing protein')]
wd_data = wd_data.merge(length_data[['protein', 'total_length']], on='protein', how='left')

# Filtrage des protéines avec longueur <= 3000
wd_data = wd_data[wd_data['total_length'] <= 3000]

# Compter le nombre de repeats WD par protéine
wd_repeat_count = wd_data.groupby('protein').size().reset_index(name='WD_repeat_count')

# On garde les protéines avec entre 4 et 8 repeats WD
initial_protein_count = wd_repeat_count['protein'].nunique()
wd_data_filtered = wd_repeat_count[(wd_repeat_count['WD_repeat_count'] >= 4) & (wd_repeat_count['WD_repeat_count'] <= 8)]
filtered_protein_count = wd_data_filtered['protein'].nunique()
proteins_filtered_out = initial_protein_count - filtered_protein_count

# Affichage des protéines restantes
print(wd_data_filtered)

# Calcul et affichage du nombre cumulé de repeats WD
total_repeats = wd_data_filtered['WD_repeat_count'].sum()
print(f"Nombre cumulé de repeats WD : {total_repeats}")

# Calcul et affichage de la moyenne des repeats WD par protéine
average_repeats = wd_data_filtered['WD_repeat_count'].mean()
print(f"Moyenne du nombre de repeats WD par protéine : {average_repeats}")

# Affichage du nombre de protéines filtrées
print(f"Nombre de protéines filtrées : {proteins_filtered_out}")

# Conversion en CSV pour lecture
wd_data_filtered.to_csv('Nbr_repeat_resultats.csv', index=False)
