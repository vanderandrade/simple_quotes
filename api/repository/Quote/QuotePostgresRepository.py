from repository.AbstractRepository import AbstractRepository
from storage import redis
from utils.definitions import QuoteAction
from utils.database import get_database_connection, get_database_cursor

class QuotePostgresRepository(AbstractRepository):
    def add(self, quote):
        if quote is None:
            raise ValueError

        if 'quote' not in quote or 'added_by' not in quote:
            raise ValueError

        try:
            con = get_database_connection()
            cur = get_database_cursor(connection=con)

            if 'quote_by' in quote:
                sql = f'INSERT INTO Quote(quote, quote_by, added_by) ' \
                      f'VALUES({quote["quote"]}, {quote["quote_by"]}, {quote["added_by"]})'
            else:
                sql = f'INSERT INTO Quote(quote, added_by) ' \
                      f'VALUES({quote["quote"]}, {quote["added_by"]})'

            cur.execute(sql)
            con.commit()

            cur.close()
            con.close()

            return True
        except:
            pass

        return False
    
    def get(self, reference):
        try:
            con = get_database_connection()
            cur = get_database_cursor(connection=con)

            sql = f'SELECT * FROM Quote WHERE id = {reference}'

            result = cur.execute(sql)

            cur.close()
            con.close()

            return result
        except:
            pass

        return None

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
        except:
            pass

        return False

    def _get_all(self, action: QuoteAction):
        try:
            con = get_database_connection()
            cur = get_database_cursor(connection=con)

            if action == QuoteAction.GET_ALL:
                sql = f'SELECT * FROM Quote '
            elif action == QuoteAction.GET_ALL_QUOTERS or \
                 action == QuoteAction.GET_ALL_QUOTES :
                sql = f'SELECT {action.value} FROM Quote '
            else:
                sql = f'SELECT * FROM Quote '

            result = cur.execute(sql)

            cur.close()
            con.close()

            return result
        except:
            pass

        return None
