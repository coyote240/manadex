import json

import tornado.web
from tornado import gen

import pymongo
from bson import json_util

import handlers


class ExpansionHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['sets']

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        future = self.collection.find(
            {}, {'_id': 0, 'code': 1, 'name': 1, 'size': 1}
        ).sort('released', pymongo.DESCENDING)

        sets = yield future.to_list(None)
        sets_json = json.dumps(sets, default=json_util.default)

        self.set_header('Content-type', 'application/json')
        self.write(sets_json)
