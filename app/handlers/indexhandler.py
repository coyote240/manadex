import handlers


class IndexHandler(handlers.BaseHandler):

    def prepare(self):
        self.ngAppModule = 'ManaDex'

    def get(self):
        self.render('index.html',
                    ngAppModule=self.ngAppModule)
