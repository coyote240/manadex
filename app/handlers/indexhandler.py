import handlers

from tornado import gen


class IndexHandler(handlers.BaseHandler):

    def prepare(self):
        self.ngAppModule = 'UserHomeModule'
        self.collection = self.settings['db_ref']['users']

    @gen.coroutine
    def get(self):
        card_refs = yield self.collection.find_one(
            {'uid': self.current_user},
            {'_id': 0, 'collection': 1})

        card_collection = self.settings['db_ref']['cards']
        future = card_collection.find(
            {'_id': {'$in': card_refs.get('collection')}},
            {'_id': 0, 'lastModified': 0, 'created': 0})
        cards = yield future.to_list(length=None)

        self.render('index.html',
                    ngAppModule=self.ngAppModule,
                    mycards=cards)
