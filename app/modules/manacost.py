import re
import tornado


class ManaCost(tornado.web.UIModule):

    costPattern = r'({[\dWUBRGCX]+\/*[WUBRGP]*})'

    def render(self, mana):
        res = re.findall(self.costPattern, mana)
        return self.render_string('modules/mana-cost-module.html',
                                  mana=res)
