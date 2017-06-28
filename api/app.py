from flask import Flask
from flask_pymongo import PyMongo
from flask import render_template

app = Flask(__name__)

app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'stock'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/')
def hello():
    stocks = list(mongo.db.top.find({}))
    return render_template('index.html', stocks=stocks)

if __name__ == '__main__':
    app.run()
