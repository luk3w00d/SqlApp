from flask import Flask, jsonify  #when using this the import Flask use a UPPER CASE
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)
                                            # always do in this sequence and config is done at the top of the code
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:password123@127.0.0.1:5432/trello'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Card(db.Model):      # This will create a table that can be viewed by the users
    __tablename__ = 'cards'   # Changes the name of the name from card to cards
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date', 'status', 'priority' )

# CLI is used define a new custom (terminal) command
@app.cli.command('create')  # To use this command, you need to write flask then ('What word used here')
def create_db():
    db.create_all()
    print("Tables created")  # This will print the table that was created

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@app.cli.command('seed')
def seed_db():
    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create the database',
            status = 'To Do',
            priority = 'High',
            date = date.today()
        ),
        Card(
            title = "SQLAlchemy",
            description = "Stage 2 - Integrate ORM",
            status = "Ongoing",
            priority = "High",
            date = date.today()
        ),
        Card(
            title = "ORM Queries",
            description = "Stage 3 - Implement several queries",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        ),
        Card(
            title = "Marshmallow",
            description = "Stage 4 - Implement Marshmallow to jsonify models",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        )
    ]

    db.session.add_all(cards)
    db.session.commit()
    print('Tables seeded')

@app.route('/cards/')
def all_cards():     # select * from all_cards
    # cards = Card.query.all()
    # print(cards)
    stmt = db.select(Card).order_by(Card.priority.desc(), Card.title)
    cards = db.session.scalars(stmt)
    return CardSchema(many=True).dump(cards)

@app.cli.command('first_card')
def first_card():     # select * from cards limit 1;
    card = Card.query.first()
    print(card)

@app.route('/') 
def index():
    return "hello world!"
