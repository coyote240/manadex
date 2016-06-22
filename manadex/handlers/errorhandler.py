import httplib
import handlers


class NotFoundHandler(handlers.BaseHandler):
    def prepare(self):
        status_code = 404
        reason = httplib.responses[status_code]
        self.set_status(status_code)
        self.render('errors/general.html',
                    status_code=status_code,
                    reason=reason)
