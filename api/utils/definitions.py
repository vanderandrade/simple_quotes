from enum import Enum

class QuoteAction(Enum):
    GET_ALL = 1
    GET_ALL_QUOTES = 'quote'
    GET_ALL_QUOTERS = 'quote_by'