from tornado import gen

import handlers


class DeckHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['decks']

    @gen.coroutine
    def get(self):
        future = self.collection.find()
        decks = yield future.to_list(None)
        self.render('decks/index.html',
                    decks=decks)


class DeckFormHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['decks']
