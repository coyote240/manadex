import re
import logging


gen_delims = r'[:\/\?#\[\]@\s]+'
sub_delims = r'[!\$&\'\(\)\*\+,;=]+'


def sanitize_name(name):
    name = re.sub(gen_delims, '-', name)
    name = re.sub(sub_delims, '', name)
    return name.lower()


def warn(msg):
    logging.warning(msg)


class SpareDict(dict):

    def __init__(self, init_dict={}, *args, **kwargs):
        for key, value in init_dict.iteritems():
            self[key] = value
        for key, value in kwargs.iteritems():
            self[key] = value

    def __setitem__(self, key, value):
        if value is not None:
            super(SpareDict, self).__setitem__(key, value)


class MetaCard(type):
    '''
    MetaCard - Card metaclass

    Provides a factory method.  Classes inheriting from Card, or any
    class that defines MetaCard as a metaclass will be available as a card
    type returned by the factory method.
    '''

    card_types = []

    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        mcs.card_types.append(cls)
        return cls

    @classmethod
    def factory(meta, card_dict):
        for card_type in meta.card_types:
            warn(card_type)
            if card_type.match(card_dict):
                return card_type(card_dict)


class CardType(object):
    def __init__(self, *args):
        self.types = args

    def __call__(self, cls):
        cls.type_tokens = self.types
        return cls


class Card(dict):
    __metaclass__ = MetaCard
    type_tokens = ()

    def __init__(self, card_dict):
        self.name = card_dict.get('name')
        self.supertype = card_dict.get('supertype')
        self.types = card_dict.get('types')
        self.subtype = card_dict.get('subtype')
        self.expansion = card_dict.get('expansion')
        self.description = card_dict.get('description')
        self.flavor_text = card_dict.get('flavorText')
        self.rarity = card_dict.get('rarity')
        self.collector_number = card_dict.get('collectorNumber')
        self.keywords = card_dict.get('keywords')

        self.created = None
        self.created_by = None

    @classmethod
    def match(cls, card_dict):
        types = tuple(card_dict.get('types'))
        return set(cls.type_tokens) >= set(types)

    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, value):
        self._types = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._sanitized_name = sanitize_name(value)

    @property
    def sanitized_name(self):
        return self._sanitized_name

    @property
    def last_modified(self):
        return self._last_modified

    @last_modified.setter
    def last_modified(self, date):
        self._last_modified = date

    @property
    def last_modified_by(self):
        return self._last_modified_by

    @last_modified_by.setter
    def last_modified_by(self, value):
        self._last_modified_by = value

    def to_dict(self):
        return SpareDict({
            'name': self.name,
            'supertype': self.supertype,
            'types': self.types,
            'subtype': self.subtype,
            'sanitized_name': self.sanitized_name,
            'expansion': self.expansion,
            'description': self.description,
            'flavorText': self.flavor_text,
            'rarity': self.rarity,
            'collectorNumber': self.collector_number,
            'keywords': self.keywords,
            'lastModified': self.last_modified,
            'lastModifiedBy': self.last_modified_by,
            'created': self.created,
            'createdBy': self.created_by
        })


class Castable(Card):
    _colors = [
        'white', 'blue', 'black', 'red',
        'green', 'colorless', 'generic']

    def __init__(self, card_dict):
        super(Castable, self).__init__(card_dict)
        self.mana_cost = card_dict.get('manaCost')

    @property
    def mana_cost(self):
        return self._mana_cost

    @mana_cost.setter
    def mana_cost(self, value):
        cost = []

        for mana in value:
            color = mana.get('color')
            value = mana.get('value')

            if color not in Castable._colors:
                raise Exception('Unknown mana color.')

            cost.append(mana)

        if len(cost) > 0:
            self._mana_cost = cost
        else:
            self._mana_cost = None

    @property
    def cmc(self):
        '''
        Converted Mana Cost
        '''
        return reduce(
            lambda x, y: x + y,
            [mana['value']
                for mana in self.mana_cost if isinstance(mana['value'], int)])

    @staticmethod
    def _cost(mana):
        '''
        '''
        pass

    def to_dict(self):
        card_dict = super(Castable, self).to_dict()
        card_dict.update({
            'manaCost': self.mana_cost
        })
        return card_dict
