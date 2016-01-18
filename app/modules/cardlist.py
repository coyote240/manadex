import tornado


class CardList(tornado.web.UIModule):

    def render(self, cards):
        return self.render_string('modules/cardlist-module.html',
                                  cards=cards)


class CardListItem(tornado.web.UIModule):

    def render(self, card):
        return self.render_string('modules/cardlist-item-module.html',
                                  card=card)
