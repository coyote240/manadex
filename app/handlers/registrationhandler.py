import os
import hashlib
import binascii

from tornado import gen

import handlers


def hash_password(password):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    return binascii.hexlify(dk)


class RegistrationHandler(handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['users']

    def get(self):
        self.render('register.html',
                    ngAppModule='ManaDex')

    @gen.coroutine
    def post(self):
        uid = self.get_argument('uid')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password-confirm')

        if password != password_confirm:
            self.send_error(status_code=400,
                            reason='Passwords must match.')
            return

        existing_user = yield self.collection.find_one({'uid': uid})
        if existing_user is not None:
            self.send_error(status_code=409,
                            reason='User name already in use.')
            return

        hashed_password = hash_password(password)
        future = self.collection.insert({'uid': uid,
                                         'password': hashed_password,
                                         'collection': [],
                                         'wishlist': []})
        id = yield future
        self.write(str(id))
