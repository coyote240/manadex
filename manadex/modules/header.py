import tornado


class Header(tornado.web.UIModule):

    def render(self):
        return self.render_string('modules/header-module.html')
