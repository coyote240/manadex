import re
import json
import logging

from tornado import gen
from bson.objectid import ObjectId

import handlers


gen_delims = r'[:\/\?#\[\]@\s+]'
sub_delims = r'[!\$&\'\(\)\*\+,;=]'


def sanitize_name(name):
    name = re.sub(gen_delims, '-', name)
    name = re.sub(sub_delims, '', name)
    return name


class CardHandler(handlers.BaseHandler):
    '''
    Card display handler

    Return a 404 when id is not found.
    '''

    def prepare(self):
        self.collection = self.settings['db_ref']['cards']

    @gen.coroutine
    def get(self, id=None):
        future = self.collection.find()
        cards = yield future.to_list(None)
        self.render('cards/index.html',
                    cards=cards)


class CardFormHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['cards']

    @gen.coroutine
    def get(self, id=None):
        card = None
        if id is not None:
            card = yield self.collection.find_one(ObjectId(id))
            if card is None:
                self.redirect('/cards')
                return

        card_json = self.encode_json(card)
        self.render('cards/form.html',
                    card=card_json)


class CardAPIHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['cards']

    def get(self):
        self.render('cards/form.html', xsrf_token=self.xsrf_token)

    @gen.coroutine
    def post(self):
        logging.warning(self.request.body)
        card = json.loads(self.request.body)

        future = self.collection.insert(card)
        id = yield future
        self.write(str(id))

    @gen.coroutine
    def put(self):
        card = json.loads(self.request.body)
        logging.warning(type(card))
        id = card.get('_id')
        del card['_id']
        logging.warning(card)

        result = yield self.collection.update({'_id': ObjectId(id)}, card)
        self.write(result)

    @gen.coroutine
    def delete(self):
        logging.warning(self.request.body)
        card = json.loads(self.request.body)
        id = card.get('_id')
        del card['_id']

        result = yield self.collection.remove({'_id': ObjectId(id)})
        self.write(result)
