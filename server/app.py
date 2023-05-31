from flask import Flask, send_file, render_template, jsonify
import pandas as pd
import os
import psycopg2
import sqlalchemy as sa
from db_setup import setup

engine = sa.create_engine('postgresql://docker:docker@postgres:5432/default')
app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    rows = pd.read_sql("select count(*) from bus", engine).iloc[0]['count']
    return render_template('index.html', rows = rows)

if __name__ == '__main__':
    setup(engine)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)