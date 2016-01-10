import re
import json
import logging

from tornado import gen

import handlers


gen_delims = r'[:\/\?#\[\]@\s]+'
sub_delims = r'[!\$&\'\(\)\*\+,;=]+'


def sanitize_name(name):
    name = re.sub(gen_delims, '-', name)
    name = re.sub(sub_delims, '', name)
    return name.lower()


class CardHandler(handlers.BaseHandler):

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
    def get(self, name=None):
        card = None
        if name is not None:
            card = yield self.collection.find_one(
                {'sanitized_name': name}, {'_id': 0})
            if card is None:
                self.redirect('/cards')
                return

        card_json = self.encode_json(card)
        self.render('cards/form.html',
                    card=card_json)


class CardAPIHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['cards']
        logging.warning(self.request.body)
        self.card = json.loads(self.request.body)

    def get(self):
        self.render('cards/form.html', xsrf_token=self.xsrf_token)

    @gen.coroutine
    def post(self):
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

    @gen.coroutine
    def put(self):
        result = yield self.collection.update(
            {'sanitized_name': self.card.get('sanitized_name'),
             'expansion': self.card.get('expansion')}, self.card)
        self.write(result)

    @gen.coroutine
    def delete(self):
        result = yield self.collection.remove(
            {'sanitized_name': self.card.get('sanitized_name')})
        self.write(result)
