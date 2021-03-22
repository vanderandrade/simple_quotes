from repository.AbstractRepository import AbstractRepository
from utils.definitions import QuoteAction
from models.model import db, Quote

class QuotePostgresRepository(AbstractRepository):
    def add(self, quote):
        if quote is None:
            raise ValueError('Impossible to add inexistent Quote object')

        if 'quote' not in quote or 'added_by' not in quote:
            raise ValueError('Required Quote properties are missing!')

        try:
            quote = Quote(
                quote=quote['quote'],
                quote_by=quote['quote_by'],
                added_by=quote['added_by'],
            )
            db.session.add(quote)
            db.session.commit()

            return True, 'OK'
        except Exception as e:
            print(f'Error: {e}')

        return False, 'Error when inserting Quote at storage'
    
    def get(self, reference):
        return self._convert_to_response(Quote.query.get(reference))

    def get_all(self):
        return self._get_all(QuoteAction.GET_ALL)

    def get_all_quotes(self):
        return self._get_all(QuoteAction.GET_ALL_QUOTES)

    def get_all_quoters(self):
        return self._get_all(QuoteAction.GET_ALL_QUOTERS)

    def delete(self, reference):
        try:
            Quote.query.filter_by(id=reference).delete()
            db.session.commit()

            return True, 'OK'
        except Exception as e:
            print(f'Error: {e}')

        return False, 'Error when deleting Quote at storage'

    def update(self, reference):
        if '_id' not in reference:
            raise ValueError('Impossible to search for the quote')

        quote = Quote.query.get(reference['_id'])
        if not quote:
            return False, 'Quote not found at storage'

        for k, v in reference.items():
            setattr(quote, k, v)

        db.session.commit()
        return True, 'OK'


    def _get_all(self, action: QuoteAction):
        try:
            if action in (QuoteAction.GET_ALL_QUOTERS, QuoteAction.GET_ALL_QUOTES):
                quotes = db.session.query(getattr(Quote, action.value)).distinct().order_by(getattr(Quote, action.value)).all()
                return [q[0] for q in quotes]
            else:
                quotes = db.session.query(Quote).order_by(Quote.id).all()
                return [self._convert_to_response(q) for q in quotes]
        except Exception as e:
            print(f'Error: {e}')

    def _convert_to_response(self, quote):
        if quote:
            quote = quote.__dict__
            if '_sa_instance_state' in quote:
                del quote['_sa_instance_state']
        
        return quote
