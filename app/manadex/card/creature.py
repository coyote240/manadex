from card import Castable, CardType


@CardType('creature')
class Creature(Castable):

    def __init__(self, card_dict):
        super(Creature, self).__init__(card_dict)
        self.power = card_dict.get('power', 0)
        self.toughness = card_dict.get('toughness', 0)

    def to_dict(self):
        card_dict = super(Creature, self).to_dict()
        card_dict.update({
            'power': self.power,
            'toughness': self.toughness
        })
        return card_dict
