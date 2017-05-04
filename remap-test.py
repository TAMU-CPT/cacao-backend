#!/usr/bin/env python
import json
import requests

# curl -X GET http://localhost:8000/api-token-auth-whoami/ -H 'Authorization: Token 50153b474566d672c14e528868e03d46c6d68818'

headers = {
    'Authorization': "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imh4ciIsInVzZXJfaWQiOjEsImVtYWlsIjoiIiwiZXhwIjoxNDk0MjYwOTYyfQ.Ius5A4yPyj0vXkt1e8jQLU_BvNyoKyLCzvFrrpDjWDQ",
}
# r = requests.get("http://localhost:8000/api-token-auth-whoami/", headers=headers)
# print(r.json())

remap_data = {
    'organism_old': "asdf",
    "organism_new": "asdf.v2",
    "refseq_old": "Miro",
    "refseq_new": "Miro.v2",
    "refseq_length": 148317,
    "changes": open('delta.tsv', 'r').read(),
    "renames": open('renames', 'r').read(),
}

r = requests.post("http://localhost:8000/jbrowse/remap", headers=headers, data=remap_data)
print(json.dumps(r.json()))
