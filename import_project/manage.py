from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(debug=True)

def main():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        main()
    manager.run()