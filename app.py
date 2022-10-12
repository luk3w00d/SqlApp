from flask import Flask  #when using this the import Flask use a UPPER CASE
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
                                            # always do in this sequence and config is done at the top of the code
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:password123@127.0.0.1:5432/trello'

db = SQLAlchemy(app)

class Card(db.Model):      # This will create a table that can be viewed by the users
    __tablename__ = 'cards'   # Changes the name of the name from card to cards
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)

# CLI is used define a new custom (terminal) command
@app.cli.command('create')  # To use this command, you need to write flask then ('What word used here')
def create_db():
    db.create_all()
    print("Tables created")  # This will print the table that was created

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables dropped')

@app.cli.command('seed')
def seed_db():
    card = Card(
        title = 'Start the project',
        description = 'Stage 1 - Creating the database',
        status = 'To Do',
        priority = 'High',
        date = date.today()
    )

    db.session.add(card)
    db.session.commit()
    print('Tables seeded')


@app.route('/') 
def index():
    return "hello world!"
