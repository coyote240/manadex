import httplib
import logging

import tornado.web


def server_settings(handler):
    handler.set_header('Server', 'BIMC Custom, Illuminated/0.1')
    handler.add_header('X-Frame-Options', 'DENY')
    handler.add_header('X-XSS-Protection', 1)
    handler.add_header('X-Content-Type-Options', 'nosniff')


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        server_settings(self)

    def write_error(self, status_code, **kwargs):
        reason = httplib.responses[status_code]
        self.render('errors/general.html',
                    status_code=status_code,
                    reason=reason)

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def info(self, message):
        logging.info(message)

    def warn(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)
