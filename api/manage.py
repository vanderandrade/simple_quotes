
import os
import pytest
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models.model import db, Quote
from app import create_app

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.shell
def shell_ctx():
    return dict(
        app=app,
        db=db,
        Quote=Quote,
    )


@manager.command
def test():
    """Runs the tests."""
    pytest.main([])


if __name__ == '__main__':
    manager.run()
