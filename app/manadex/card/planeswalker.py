import card


class Planeswalker(card.Castable):

    @classmethod
    def match(cls, card_dict):
        return card_dict.get('type') == 'planeswalker'

    def __init__(self, card_dict):
        super(Planeswalker, self).__init__(card_dict)
        self.abilities = card_dict.get('planeswalkerAbilities', [])
        self.loyalty = card_dict.get('loyalty', 0)

    @property
    def abilities(self):
        return self._abilities

    @abilities.setter
    def abilities(self, value):
        self._abilities = []

        for ability in value:
            rules = ability.get('rules')
            cost = ability.get('cost')
            self._abilities.append({
                'rules': rules,
                'cost': cost})

    def to_dict(self):
        card_dict = super(Planeswalker, self).to_dict()
        card_dict.update({
            'abilities': self.abilities,
            'loyalty': self.loyalty
        })
        return card_dict
