import tornado


class DeckList(tornado.web.UIModule):

    def creatures(self, cards):
        creature_types = ['creature', 'legendary creature']
        return [card for card in cards if card['type'] in creature_types]

    def sorceries(self, cards):
        return [card for card in cards if card['type'] in ['sorcery']]

    def instants(self, cards):
        return [card for card in cards if card['type'] in ['instant']]

    def render(self, cards):
        creatures = self.creatures(cards)
        sorceries = self.sorceries(cards)
        instants = self.instants(cards)

        return self.render_string('modules/decklist-module.html',
                                  creatures=creatures,
                                  instants=instants,
                                  sorceries=sorceries)
