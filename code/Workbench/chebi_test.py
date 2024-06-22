import requests
import json


def inspect_chebi_response(chebi_id):
    url = f"https://www.ebi.ac.uk/chebi/ws/rest/chebiId/{chebi_id}"
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed to retrieve data for {chebi_id}")


# Replace 'CHEBI:58115' with any ChEBI ID you want to inspect
inspect_chebi_response('CHEBI:58115')
