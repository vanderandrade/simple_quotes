import os

class DeployConfig(object):
    DEBUG = True
    pguser = os.environ.get('PGUSER')
    pgpass = os.environ.get('PGPASSWORD')
    pghost = os.environ.get('PGHOST')
    pgport = os.environ.get('PGPORT')
    pgdb = os.environ.get('PGDATABASE')
    SQLALCHEMY_DATABASE_URI = f'postgres://{pguser}:{pgpass}@{pghost}:{pgport}/{pgdb}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False