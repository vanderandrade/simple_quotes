from repository.AbstractRepository import AbstractRepository
from storage import redis
from utils.definitions import QuoteAction
from utils.database import get_database_connection, get_database_cursor
from models.model import db, Quote

class QuotePostgresRepository(AbstractRepository):
    def add(self, quote):
        if quote is None:
            raise ValueError

        if 'quote' not in quote or 'added_by' not in quote:
            raise ValueError

        try:
            quote = Quote(
                quote=quote['quote'],
                quote_by=quote['quote_by'],
                added_by=quote['added_by'],
            )
            db.session.add(quote)
            db.session.commit()

            return True
        except Exception as e:
            print(f'Error: {e}')

        return False
    
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
            con = get_database_connection()
            cur = get_database_cursor(connection=con)

            sql = f'DELETE FROM Quote WHERE id = {reference} '

            cur.execute(sql)
            con.commit()

            cur.close()
            con.close()

            return True
        except Exception as e:
            print(f'Error: {e}')

        return False

    def _get_all(self, action: QuoteAction):
        try:
            if action == QuoteAction.GET_ALL:
                quotes = db.session.query(Quote).all()
                return [self._convert_to_response(q) for q in quotes]
            elif action == QuoteAction.GET_ALL_QUOTERS or \
                 action == QuoteAction.GET_ALL_QUOTES :
                quotes = db.session.query(getattr(Quote, action.value)).all()
                return [q[0] for q in quotes]
            else:
                quotes = db.session.query(Quote).all()
                return [self._convert_to_response(q) for q in quotes]
        except Exception as e:
            print(f'Error: {e}')


    def _convert_to_response(self, quote):
        if quote:
            quote = quote.__dict__
            if '_sa_instance_state' in quote:
                del quote['_sa_instance_state']
        
        return quote
