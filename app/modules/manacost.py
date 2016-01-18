import tornado


class ManaCost(tornado.web.UIModule):

    def render(self, mana):
        return self.render_string('modules/mana-cost-module.html',
                                  mana=mana)
