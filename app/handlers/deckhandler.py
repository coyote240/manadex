import json
import datetime

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


class DeckAPIHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['decks']

    @property
    def card_collection(self):
        return self.settings['db_ref']['cards']

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        '''
        Create a new deck.
        '''
        deck = json.loads(self.request.body)
        deck['created'] = datetime.datetime.utcnow()
        deck['sanitized_name'] = handlers.sanitize_name(
            deck.get('name'))

        existing = yield self.collection.find_one(
            {'sanitized_name': deck.get('sanitized_name')})
        if existing is not None:
            self.send_error(status_code=409,
                            reason='A deck with that name already exists.')
            return

        sanitized_names = [card.get('name') for card in deck.get('cards')]
        future = self.card_collection.find(
            {'sanitized_name': {'$in': sanitized_names}},
            {'_id': 1})
        card_refs = yield future.to_list(length=None)

        cards = zip(
            [card.get('_id') for card in card_refs],
            [card.get('quantity') for card in deck.get('cards')])
        cards = [{'id': _id, 'quantity': quantity} for _id, quantity in cards]
        deck['cards'] = cards

        future = self.collection.insert(deck)

        id = yield future
        self.write({
            'id': str(id),
            'sanitized_name': deck.get('sanitized_name')})

    @tornado.web.authenticated
    @gen.coroutine
    def put(self):
        '''
        Add a card to a deck, or update features.
        '''
        pass

    @tornado.web.authenticated
    @gen.coroutine
    def delete(self):
        '''
        Does this delete a card from a deck, or a whole deck?
        Maybe deck documents should be updated wholesale with each adjustment?
        And this method should only be used to delete decks?
        '''
        pass
