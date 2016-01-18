#!/usr/bin/env python

import signal
import logging

import motor

import tornado.web
import tornado.ioloop
import tornado.autoreload
from tornado.httpserver import HTTPServer
from tornado.options import define, options

import handlers
import modules


class Application(tornado.web.Application):

    def __init__(self):
        self.init_options()
        self.init_handlers()
        self.init_signal_handlers()

        settings = self.init_settings()

        tornado.web.Application.__init__(self, self.handlers, **settings)

    def init_options(self):
        define('port', type=int,
               help='The port on which this app will listen.')
        define('static_path', help='Location of static assets.')
        define('template_path', help='Location of template files.')
        define('db_name', help='Name of database.')
        define('db_path', help='Path to mongodb instance.')
        define('cookie_secret', help='Cookie secret key')
        define('xsrf_cookies', default=True)
        define('config', help='Path to config file',
               callback=lambda path: options.parse_config_file(path,
                                                               final=False))
        options.parse_command_line()

    def init_settings(self):
        db_client = motor.MotorClient(options.db_path)
        db_ref = db_client[options.db_name]

        settings = {
            'debug': True,
            'db_ref': db_ref,
            'static_path': options.static_path,
            'template_path': options.template_path,
            'ui_modules': modules,
            'static_handler_class': handlers.BaseStaticHandler,
            'default_handler_class': handlers.NotFoundHandler,
            'xsrf_cookies': options.xsrf_cookies,
            'login_url': '/',
            'cookie_secret': options.cookie_secret}

        return settings

    def init_handlers(self):
        self.handlers = [
            (r'/', handlers.IndexHandler),
            (r'/auth', handlers.AuthHandler),
            (r'/logout', handlers.AuthHandler, {'action': 'logout'}),
            (r'/register', handlers.RegistrationHandler),
            (r'/cards/new', handlers.CardFormHandler),
            (r'/cards/edit/([a-zA-Z0-9-]*)', handlers.CardFormHandler),
            (r'/cards(/?[a-zA-Z0-9]*)', handlers.CardHandler),
            (r'/api/cards', handlers.CardAPIHandler)]

    def init_signal_handlers(self):
        signal.signal(signal.SIGINT, self.interrupt_handler)
        # check for windows signal not existing
        if getattr(signal, 'SIGQUIT', None):
            signal.signal(signal.SIGQUIT, self.interrupt_handler)
        #else:
        #    signal.signal(signal.SIGTERM, self.interrupt_handler)

    def interrupt_handler(self, signum, frame):
        logging.info('Shutting down server...')
        tornado.ioloop.IOLoop.instance().add_callback_from_signal(
            lambda: tornado.ioloop.IOLoop.instance().stop())

    def start(self):
        server = HTTPServer(self)
        server.listen(options.port)

        logging.info('Starting server...')
        tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    app = Application()
    app.start()
