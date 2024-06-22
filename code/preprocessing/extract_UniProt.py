'''python file to rub tmux from jupyter notebook.'''
from rdkit import RDLogger
import pandas as pd
import numpy as np
from os.path import join
import os
import urllib.parse
import urllib.request
from Bio.UniProt.GOA import _gpa11iterator
import gzip
import pickle

import warnings
warnings.filterwarnings('ignore')


# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning,
                        message=".*Chem.MolFromInchi.*")
warnings.filterwarnings("ignore", category=UserWarning,
                        message=".*SettingWithCopyWarning.*")
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


# Suppress RDKit warnings
lg = RDLogger.logger()
lg.setLevel(RDLogger.CRITICAL)

df = pd.read_pickle(join("..", "..", "data", "GOA",
                    "go_terms", "df_GO_with_substrates.pkl"))
transporter_go_terms = list(set(df["GO ID"]))
filename = join("..", "..", "data", "GOA", "goa_uniprot_all.gpa.gz")

# Initialize variables
run = 0
batch_size = 10**6
df_GO_UID = pd.DataFrame(
    columns=["Uniprot ID", "GO Term", 'ECO_Evidence_code'])

overall_count = 0
continuing = False

with gzip.open(filename, 'rt') as fp:
    for annotation in _gpa11iterator(fp):
        overall_count += 1
        if overall_count >= run * batch_size and overall_count < (run + 1) * batch_size:
            # Extract data
            UID = annotation['DB_Object_ID']
            GO_ID = annotation['GO_ID']
            ECO_Evidence_code = annotation["ECO_Evidence_code"]
            if GO_ID in transporter_go_terms:
                df_GO_UID = pd.concat([df_GO_UID, pd.DataFrame([{
                    "Uniprot ID": UID,
                    "GO Term": GO_ID,
                    'ECO_Evidence_code': ECO_Evidence_code
                }])], ignore_index=True)
        else:
            # Save the current batch to a pickle file
            df_GO_UID.to_pickle(
                join("..", "..", "data", "GOA", "GO_UID_mapping", f"df_GO_UID_part_{run}.pkl"))
            # Reset the DataFrame for the next batch
            df_GO_UID = pd.DataFrame(
                columns=["Uniprot ID", "GO Term", 'ECO_Evidence_code'])
            run += 1

            # Make sure to include the current annotation in the new batch if it's part of the next run
            if overall_count >= run * batch_size and overall_count < (run + 1) * batch_size:
                UID = annotation['DB_Object_ID']
                GO_ID = annotation['GO_ID']
                ECO_Evidence_code = annotation["ECO_Evidence_code"]
                if GO_ID in transporter_go_terms:
                    df_GO_UID = pd.concat([df_GO_UID, pd.DataFrame([{
                        "Uniprot ID": UID,
                        "GO Term": GO_ID,
                        'ECO_Evidence_code': ECO_Evidence_code
                    }])], ignore_index=True)

# Save the final batch if any annotations were processed in the last run
if not df_GO_UID.empty:
    df_GO_UID.to_pickle(join("..", "..", "data", "GOA",
                        "GO_UID_mapping", f"df_GO_UID_part_{run}.pkl"))
