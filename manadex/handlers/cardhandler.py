import re
import json
import datetime

import tornado.web
from tornado import gen

from bson import json_util

import handlers
from card import Card


class BaseCardHandler(handlers.BaseHandler):

    def prepare(self):
        self.ngAppModule = 'ManaDex'
        self.collection = self.settings['db_ref']['cards']

    @gen.coroutine
    def get_card(self, name):
        card = yield self.collection.find_one(
            {'sanitized_name': name}, {'_id': 0})
        raise gen.Return(card)

    @gen.coroutine
    def add_to_collection(self, card_id):
        user_collection = self.settings['db_ref']['users']
        result = yield user_collection.update(
            {'uid': self.current_user},
            {'$addToSet': {'collection': card_id}})
        raise gen.Return(result)


class CardHandler(BaseCardHandler):

    symbols = {
        'T': '<span class="tapped"></span>',
        'W': '<span class="mana white"></span>',
        'U': '<span class="mana blue"></span>',
        'B': '<span class="mana black"></span>',
        'R': '<span class="mana red"></span>',
        'G': '<span class="mana green"></span>',
        'C': '<span class="mana colorless"></span>'
    }

    def replace_token(self, match):
        value = match.group(1)
        replacement = CardHandler.symbols.get(value)

        if replacement is None:
            return '<span class="mana generic">{0}</span>'.format(value)
        return replacement

    def rules_display(self, rules):
        rules = re.sub(r'\{([A-Z0-9]+)\}', self.replace_token, rules)
        rules = re.sub(r'\n+', '<br/>', rules)
        return rules

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, name=None):
        start = self.get_argument('start', default=0)
        start = int(start)
        limit = self.get_argument('limit', default=20)
        limit = int(limit)
        #sort = self.get_argument('sort', default=None)

        if name:
            card = yield self.get_card(name)
            if card is None:
                self.send_error(status_code=404, reason="Card not found.")
                return
            else:
                self.render('cards/view.html',
                            ngAppModule=self.ngAppModule,
                            rules_display=self.rules_display,
                            card=card)
                return

        future = self.collection.find().limit(limit).skip(start)
        cards = yield future.to_list(None)
        self.render('cards/index.html',
                    ngAppModule='CardIndexModule',
                    cards=cards, start=start, limit=limit)


class CardFormHandler(BaseCardHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, name=None):
        card = None
        if name is not None:
            card = yield self.get_card(name)
            if card is None:
                self.send_error(status_code=404, reason="Card not found.")
                return

        card_json = json.dumps(card, default=json_util.default)
        self.render('cards/form.html',
                    ngAppModule='CardFormModule',
                    card=card_json)


class CardLookupHandler(BaseCardHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        field = self.get_argument('field')
        value = self.get_argument('value')

        cursor = self.collection.find(
            {field: {'$regex': r'^{0}'.format(value), '$options': 'i'}},
            {'_id': 0, field: 1, 'sanitized_name': 1})
        found = yield cursor.to_list(length=None)
        results = [{
            field: item.get(field),
            'sanitized_name': item.get('sanitized_name')} for item in found]

        self.set_header('Content-type', 'application/json')
        self.write({'results': results})


class CardAPIHandler(BaseCardHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, name=None):
        card = None
        if name is not None:
            card = yield self.get_card(name)
            if card is None:
                self.send_error(status_code=404, reason="Card not found.")
                return

        card_json = json.dumps(card, default=json_util.default)
        self.set_header('Content-type', 'application/json')
        self.write(card_json)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        card_dict = json.loads(self.request.body)

        card = Card.factory(card_dict)
        card.created = datetime.datetime.utcnow()
        card.created_by = self.current_user
        card.last_modified = datetime.datetime.utcnow()
        card.last_modified_by = self.current_user

        existing = yield self.collection.find_one(
            {'sanitized_name': card.sanitized_name,
             'expansion': card.expansion})

        if existing is not None:
            self.send_error(status_code=409, reason='Card already exists')
            return

        future = self.collection.insert(card.to_dict())
        id = yield future

        if card_dict.get('inMyCollection'):
            self.add_to_collection(id)

        self.write(str(id))

    @tornado.web.authenticated
    @gen.coroutine
    def put(self):
        card_dict = json.loads(self.request.body)

        card = Card.factory(card_dict)
        card.last_modified = datetime.datetime.utcnow()
        card.last_modified_by = self.current_user

        existing = yield self.collection.find_one(
            {'sanitized_name': card.sanitized_name,
             'expansion': card.expansion},
            {'_id': 1})

        if existing is None:
            self.send_error(status_code=404,
                            reason='Card does not exist')
            return

        result = yield self.collection.update(
            {'sanitized_name': card.sanitized_name,
             'expansion': card.expansion},
            {'$set': card.to_dict()})

        if card_dict.get('inMyCollection'):
            id = existing.get('_id')
            self.add_to_collection(id)

        self.write(result)

    @tornado.web.authenticated
    @gen.coroutine
    def delete(self):
        card = json.loads(self.request.body)
        result = yield self.collection.remove(
            {'sanitized_name': card.get('sanitized_name')})
        self.write(result)
