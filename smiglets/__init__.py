from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['ELASTICSEARCH_URL'] = 'http://localhost:9200'
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])
db = SQLAlchemy(app)

from smiglets import routes