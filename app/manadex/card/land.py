import card


class Land(card.Card):

    @classmethod
    def match(cls, card_dict):
        return card_dict.get('type') == 'land'
