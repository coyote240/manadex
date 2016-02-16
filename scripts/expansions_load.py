#!/usr/bin/env python

import re
import csv
import datetime
from pymongo import MongoClient


docs = []
code_pattern = r'([a-zA-Z0-9]+)\s*\(([a-zA-Z0-9]+)\)'

with open('Sets.csv', 'rb') as csvfile:
    setsreader = csv.DictReader(
        csvfile,
        fieldnames=('released', 'name', 'code', 'size', 'type', 'notes'))

    for row in setsreader:
        year, month = row.get('released').split('-')
        released = datetime.datetime(int(year), int(month), 1)

        m = re.match(code_pattern, row['code'])
        if m is not None:
            code, secondary_code = m.group(1, 2)
        else:
            code = row['code']
            secondary_code = None

        doc = {
            'released': released,
            'name': row['name'],
            'code': code,
            'secondary_code': secondary_code,
            'size': row['size'],
            'type': row['type'],
            'notes': row['notes']
        }
        docs.append(doc)

client = MongoClient()
db = client['manadex']

result = db.sets.insert(docs)
print result.inserted_ids
