import handlers


class AuthHandler(handlers.BaseHandler):
    def initialize(self, action=None):
        self.action = action
        self.collection = self.settings['db_ref']['users']

    def get(self):
        if self.action is 'logout':
            self.clear_cookie('user')
            self.redirect('/')
        else:
            self.render('login.html')

    def post(self):
        uid = self.get_argument('uid')
        self.set_secure_cookie('user', uid)
        self.redirect('/')
