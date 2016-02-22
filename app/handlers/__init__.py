import re

from basehandler import BaseHandler, BaseStaticHandler, JSONEncoder
from authhandler import AuthHandler
from registrationhandler import RegistrationHandler
from errorhandler import NotFoundHandler
from indexhandler import IndexHandler
from cardhandler import (CardHandler, CardFormHandler, CardAPIHandler,
                         CardLookupHandler)
from deckhandler import DeckHandler, DeckFormHandler, DeckAPIHandler
from collectionhandler import CollectionHandler
from expansionhandler import ExpansionHandler


gen_delims = r'[:\/\?#\[\]@\s]+'
sub_delims = r'[!\$&\'\(\)\*\+,;=]+'


def sanitize_name(name):
    name = re.sub(gen_delims, '-', name)
    name = re.sub(sub_delims, '', name)
    return name.lower()


__all__ = ['BaseHandler', 'BaseStaticHandler', 'JSONEncoder', 'AuthHandler',
           'RegistrationHandler', 'NotFoundHandler', 'IndexHandler',
           'CardHandler', 'CardFormHandler', 'CardAPIHandler',
           'CardLookupHandler', 'DeckHandler', 'DeckFormHandler',
           'CollectionHandler', 'DeckAPIHandler', 'ExpansionHandler']
