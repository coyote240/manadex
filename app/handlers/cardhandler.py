import re
import json
import logging
import datetime

import tornado.web
from tornado import gen

from bson import json_util

import handlers


gen_delims = r'[:\/\?#\[\]@\s]+'
sub_delims = r'[!\$&\'\(\)\*\+,;=]+'


def sanitize_name(name):
    name = re.sub(gen_delims, '-', name)
    name = re.sub(sub_delims, '', name)
    return name.lower()


class BaseCardHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['cards']


class CardHandler(BaseCardHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, name=None):
        if name:
            card = yield self.collection.find_one(
                {'sanitized_name': name}, {'_id': 0})
            if card is None:
                self.send_error(status_code=404, reason="Card not found.")
                return
            else:
                self.render('cards/view.html',
                            card=card)
                return

        future = self.collection.find()
        cards = yield future.to_list(None)
        self.render('cards/index.html',
                    cards=cards)


class CardFormHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['cards']

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, name=None):
        card = None
        if name is not None:
            card = yield self.collection.find_one(
                {'sanitized_name': name}, {'_id': 0})
            if card is None:
                self.redirect('/cards')
                return

        card_json = json.dumps(card, default=json_util.default)
        self.render('cards/form.html',
                    card=card_json)


class CardAPIHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['cards']
        logging.warning(self.request.body)

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        query = self.get_argument('q')
        cursor = self.collection.find(
            {'name': {'$regex': r'^{0}'.format(query), '$options': 'i'}},
            {'_id': 0})
        found = yield cursor.to_list(length=None)
        self.write(self.encode_json(found))

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        self.card = json.loads(self.request.body)
        self.card['lastModified'] = datetime.datetime.utcnow()
        self.card['lastModifiedBy'] = self.current_user
        self.card['sanitized_name'] = sanitize_name(self.card.get('name'))

        existing = yield self.collection.find_one(
            {'sanitized_name': self.card.get('sanitized_name'),
             'expansion': self.card.get('expansion')})
        logging.warning(existing)
        if existing is not None:
            self.send_error(status_code=409, reason='Card already exists')
            return

        future = self.collection.insert(self.card)
        id = yield future
        self.write(str(id))

    @tornado.web.authenticated
    @gen.coroutine
    def put(self):
        self.card = json.loads(self.request.body)
        self.card['lastModified'] = datetime.datetime.utcnow()
        self.card['lastModifiedBy'] = self.current_user

        result = yield self.collection.update(
            {'sanitized_name': self.card.get('sanitized_name'),
             'expansion': self.card.get('expansion')}, self.card)
        self.write(result)

    @tornado.web.authenticated
    @gen.coroutine
    def delete(self):
        result = yield self.collection.remove(
            {'sanitized_name': self.card.get('sanitized_name')})
        self.write(result)
