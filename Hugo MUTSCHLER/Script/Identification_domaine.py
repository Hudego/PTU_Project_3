import pandas as pd

excel_file = 'WD_extracted_data.xlsx'
df = pd.read_excel(excel_file, sheet_name='protein_length')

# Liste des protéines ayant plus d'un domaine et leur nombre de domaines
manual_domains = {
    'EMAL5_HUMAN': 6, 'EMAL6_HUMAN': 6, 'APAF_HUMAN': 2, 'CFA_HUMAN': 2, 'TEP1_HUMAN': 3,
    'STB5L_HUMAN': 2, 'STXB5_HUMAN': 2, 'CF251_HUMAN': 2, 'L2GL_HUMAN': 2, 'PWP2_HUMAN': 2,
    'ELP2_HUMAN': 2, 'UTP4_HUMAN': 2, 'NWD1_HUMAN': 2, 'EMAL2_HUMAN': 2, 'EMAL1_HUMAN': 2,
    'TBL3_HUMAN': 2, 'GEMI5_HUMAN': 2, 'MABP1_HUMAN': 2, 'WDR90_HUMAN': 4, 'WDR6_HUMAN': 3,
    'WDR3_HUMAN': 2, 'WDR36_HUMAN': 2, 'WDR64_HUMAN': 2, 'WDR62_HUMAN': 2, 'WDR27_HUMAN': 2,
    'WDR11_HUMAN': 2
}

# Exclusion des protéines de la famille DMX
df = df[~df['protein'].isin(['DMXL1_HUMAN','DMXL2_HUMAN'])]

# Création des colonnes 'nb_domains' et 'nb_repeats'
df['nb_domains'] = df['protein'].apply(lambda x: manual_domains.get(x, 1))
df['nb_repeats'] = df['nb_domains'] * 7  # Calcul des repeats (7 repeats par domaine)

output_file = 'Domaines_WD_par_protéines.xlsx'
df[['protein', 'nb_domains', 'nb_repeats']].to_excel(output_file, index=False)

print(f"Fichier Excel généré : {output_file}")


