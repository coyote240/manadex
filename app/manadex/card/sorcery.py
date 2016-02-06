import card


class Sorcery(card.Castable):

    @classmethod
    def match(cls, card_dict):
        return card_dict.get('type') == 'sorcery'
