import json

import tornado.web
from tornado import gen

from bson import json_util

import handlers


class BaseCollectionHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['users']


class CollectionHandler(BaseCollectionHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        '''
        Return a list of cards representing this user's collection.
        '''
        card_refs = yield self.collection.find_one(
            {'uid': self.current_user},
            {'_id': 0, 'collection': 1})

        if card_refs is None:
            self.send_error(status_code=404, reason='Collection not found.')
            return

        card_collection = self.settings['db_ref']['cards']
        future = card_collection.find(
            {'_id': {'$in': card_refs.get('collection')}},
            {'_id': 0})
        cards = yield future.to_list(length=None)

        cards_json = json.dumps(cards, default=json_util.default)

        self.set_header('Content-type', 'application/json')
        self.write(cards_json)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self, expansion=None, name=None):
        '''
        Add a card to this user's collection.
        '''
        user = yield self.collection.find_one({'uid': self.current_user})
        if user is None:
            self.send_error(status_code=404,
                            reason='User record not found.')
            return

        card_collection = self.settings['db_ref']['cards']
        card = yield card_collection.find_one(
            {'sanitized_name': name}, {'expansion': expansion})
        if card is None:
            self.send_error(status_code=404,
                            reason='Card not found.')
            return

        result = yield self.collection.update(
            {'uid': self.current_user},
            {'$addToSet': {'collection': card.get('_id')}})

        self.write({'id': str(result)})

    @tornado.web.authenticated
    @gen.coroutine
    def delete(self, name=None):
        '''
        Remove a card from this user's collection.
        '''
        pass
