import json
import datetime

import tornado.web
from tornado import gen

import handlers


class BaseDeckHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['decks']

    @property
    def card_collection(self):
        return self.settings['db_ref']['cards']

    @gen.coroutine
    def get_deck(self, name):
        deck = yield self.collection.find_one(
            {'sanitized_name': name,
             'createdBy': self.current_user}, {'_id': 0})
        raise gen.Return(deck)

    @gen.coroutine
    def get_decks(self):
        future = self.collection.find(
            {'createdBy': self.current_user}, {'_id': 0})
        decks = yield future.to_list(None)
        raise gen.Return(decks)

    @gen.coroutine
    def get_card_ids(self, deck):
        cards = deck.get('cards')
        sanitized_names = [card.get('sanitized_name') for card in cards]
        future = self.card_collection.find(
            {'sanitized_name': {'$in': sanitized_names}},
            {'_id': 1})
        ids = yield future.to_list(None)
        raise gen.Return(ids)

    @gen.coroutine
    def get_cards(self, deck):
        ids = [card.get('id') for card in deck.get('cards')]
        future = self.card_collection.find(
            {'_id': {'$in': ids}},
            {'_id': 0})
        cards = yield future.to_list(None)
        raise gen.Return(cards)


class DeckHandler(BaseDeckHandler):

    def prepare(self):
        super(DeckHandler, self).prepare()
        self.ngAppModule = 'ManaDex'

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, name=None):
        if name:
            deck = yield self.get_deck(name)
            if deck is None:
                self.send_error(status_code=404, reason="Deck not found.")
                return
            else:
                cards = yield self.get_cards(deck)
                self.render('decks/view.html',
                            ngAppModule=self.ngAppModule,
                            deck=deck,
                            cards=cards)
                return

        decks = yield self.get_decks()
        self.info(decks)
        self.render('decks/index.html',
                    ngAppModule=self.ngAppModule,
                    decks=decks)


class DeckFormHandler(BaseDeckHandler):

    def prepare(self):
        super(DeckFormHandler, self).prepare()
        self.ngAppModule = 'DeckBuilderModule'

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, name=None):
        '''
        Get a deck by name, or all decks if no name is specified.
        '''
        deck = None
        if name is not None:
            deck = yield self.get_deck(name)
            if deck is None:
                self.send_error(status_code=404, reason='Deck not found.')
                return

        decks = yield self.get_decks()

        deck_json = self.encode_json(deck)
        self.render('decks/form.html',
                    ngAppModule=self.ngAppModule,
                    deck=deck_json,
                    count=len(decks))


class DeckAPIHandler(BaseDeckHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['decks']

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        '''
        Create a new deck.
        '''
        deck = json.loads(self.request.body)
        deck['created'] = datetime.datetime.utcnow()
        deck['createdBy'] = self.current_user
        deck['sanitized_name'] = handlers.sanitize_name(
            deck.get('name'))

        existing = yield self.get_deck(deck.get('sanitized_name'))
        if existing is not None:
            self.send_error(status_code=409,
                            reason='A deck with that name already exists.')
            return

        card_refs = yield self.get_card_ids(deck)

        # this is gross, fix this
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
        deck = json.loads(self.request.body)
        deck['lastModified'] = datetime.datetime.utcnow()
        deck['createdBy'] = self.current_user

        card_refs = yield self.get_card_ids(deck)

        cards = zip(
            [card.get('_id') for card in card_refs],
            [card.get('quantity') for card in deck.get('cards')])
        cards = [{'id': _id, 'quantity': quantity} for _id, quantity in cards]
        deck['cards'] = cards

        result = yield self.collection.update(
            {'sanitized_name': deck.get('sanitized_name'),
             'createdBy': self.current_user}, deck)

        result['sanitized_name'] = deck.get('sanitized_name')
        self.write(result)

    @tornado.web.authenticated
    @gen.coroutine
    def delete(self):
        '''
        Does this delete a card from a deck, or a whole deck?
        Maybe deck documents should be updated wholesale with each adjustment?
        And this method should only be used to delete decks?
        '''
        pass
