from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Configurations
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)

import interview_analysis.views