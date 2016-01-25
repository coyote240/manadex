import tornado.web
from tornado import gen

import handlers


class DeckHandler(handlers.BaseHandler):

    def prepare(self):
        self.ngAppModule = 'ManaDex'
        self.collection = self.settings['db_ref']['decks']

    @gen.coroutine
    def get(self, id=None):
        future = self.collection.find()
        decks = yield future.to_list(None)
        self.render('decks/index.html',
                    ngAppModule=self.ngAppModule,
                    decks=decks)


class DeckFormHandler(handlers.BaseHandler):

    def prepare(self):
        self.ngAppModule = 'DeckBuilderModule'
        self.collection = self.settings['db_ref']['decks']

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, name=None):
        '''
        Get a deck by name, or all decks if no name is specified.
        '''
        deck = None
        if name is not None:
            deck = yield self.collection.find_one(
                {'sanitized_name': name}, {'_id': 0})
            if deck is None:
                self.redirect('/decks')
                return

        deck_json = self.encode_json(deck)
        self.render('decks/form.html',
                    ngAppModule=self.ngAppModule,
                    deck=deck_json)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self, name):
        '''
        Create a new deck.
        '''
        pass

    @tornado.web.authenticated
    @gen.coroutine
    def put(self):
        '''
        Add a card to a deck, or update features.
        '''
        pass
