import json
import logging

from tornado import gen
import handlers


class CardHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['cards']

    def get(self):
        self.render('cards/index.html',
                    xsrf_token=self.xsrf_token,
                    status_code=200,
                    reason='Ok')

    @gen.coroutine
    def post(self):
        logging.warning(self.request.body)
        card = json.loads(self.request.body)

        future = self.collection.insert(card)
        id = yield future
        self.write(str(id))

    def put(self):
        pass

    def delete(self):
        pass
