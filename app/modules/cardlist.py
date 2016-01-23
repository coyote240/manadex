import tornado


class CardList(tornado.web.UIModule):

    def render(self, cards, start=0, limit=20):
        return self.render_string('modules/cardlist-module.html',
                                  cards=cards, start=start, limit=limit)


class CardListItem(tornado.web.UIModule):

    def render(self, card):
        return self.render_string('modules/cardlist-item-module.html',
                                  card=card)
