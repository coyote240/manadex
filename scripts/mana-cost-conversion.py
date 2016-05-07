#!/usr/bin/env python

from pymongo import MongoClient


client = MongoClient()
db = client['manadex']


keys = {
    'white': '{W}',
    'blue': '{U}',
    'black': '{B}',
    'red': '{R}',
    'green': '{G}',
    'colorless': '{C}'}


def convertCost(cost):
    converted = []
    for c in cost:
        if c['color'] == 'generic':
            converted.append('{{{0}}}'.format(c['value']))
        else:
            symbol = keys.get(c['color'])
            converted.append(symbol * int(c['value']))

    return ''.join(converted)

if __name__ == '__main__':
    cursor = db.cards.find()
    for card in cursor:
        _id = card.get('_id')
        manaCost = card.get('manaCost')

        if manaCost is not None:
            if type(manaCost) is not list:
                continue
            cost = convertCost(manaCost)

            db.cards.update(
                {'_id': _id},
                {'$set': {
                    'manaCost': cost}})
