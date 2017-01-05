import os
from app import create_app, db
from app.models import User, Order, Contact, Product, Subscription, Mobile, Transaction
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


def make_shell_context():
    return dict(app=app, db=db, User=User, Order=Order, Contact=Contact, Product=Product,
                Subscription=Subscription, Mobile=Mobile, Transaction=Transaction)


app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
