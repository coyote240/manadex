import json
import datetime

import tornado.web
from tornado import gen

from bson import json_util

import handlers
from manadex.card import Card


class BaseCardHandler(handlers.BaseHandler):

    def prepare(self):
        self.ngAppModule = 'ManaDex'
        self.collection = self.settings['db_ref']['cards']

    @gen.coroutine
    def get_card(self, name):
        card = yield self.collection.find_one(
            {'sanitized_name': name}, {'_id': 0})
        raise gen.Return(card)


class CardHandler(BaseCardHandler):

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


class CardAPIHandler(BaseCardHandler):

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
        self.write(str(id))

    @tornado.web.authenticated
    @gen.coroutine
    def put(self):
        card_dict = json.loads(self.request.body)

        card = Card.factory(card_dict)
        card.last_modified = datetime.datetime.utcnow()
        card.last_modified_by = self.current_user

        result = yield self.collection.update(
            {'sanitized_name': card.sanitized_name,
             'expansion': card.expansion},
            {'$set': card.to_dict()})
        self.write(result)

    @tornado.web.authenticated
    @gen.coroutine
    def delete(self):
        card = json.loads(self.request.body)
        result = yield self.collection.remove(
            {'sanitized_name': card.get('sanitized_name')})
        self.write(result)
