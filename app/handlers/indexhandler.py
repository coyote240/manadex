import handlers


class IndexHandler(handlers.BaseHandler):

    def get(self):
        self.render('index.html',
                    title='Welcome to the Enclave',
                    status_code=200,
                    reason='Ok')
