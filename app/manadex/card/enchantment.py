import card


class Enchantment(card.Castable):

    @classmethod
    def match(cls, card_dict):
        return card_dict.get('type') == 'enchantment'
