import requests
import pandas as pd


def get_smiles_from_chebi(chebi_id):
    url = f"https://www.ebi.ac.uk/chebi/ws/rest/chemicalEntity/{chebi_id}"
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'SMILES' in data:
            return data['SMILES']
        elif 'ChemicalData' in data and 'SMILES' in data['ChemicalData']:
            return data['ChemicalData']['SMILES']
    return None


# Load ChEBI IDs from CSV file
input_csv = '/data_link/servilla/SPOT2/data/Uniprot/Unique_CHEBI_IDs.csv'
df = pd.read_csv(input_csv)

# Ensure the column containing ChEBI IDs is correctly named
chebi_ids = df['molecule ID']

# Create a DataFrame to store the results
results = []

for chebi_id in chebi_ids:
    smiles = get_smiles_from_chebi(chebi_id)
    results.append({'ChEBI ID': chebi_id, 'SMILES': smiles})

results_df = pd.DataFrame(results)

# Save the results to a new CSV file
output_csv = 'chebi_smiles.csv'
results_df.to_csv(output_csv, index=False)

print(results_df)
