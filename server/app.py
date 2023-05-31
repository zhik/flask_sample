from flask import Flask, send_file, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import psycopg2
import sqlalchemy as sa
from db_setup import setup

engine = sa.create_engine('postgresql://docker:docker@postgres:5432/default')
app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/')
def home():
    rows = pd.read_sql("select count(*) from bus", engine).iloc[0]['count']
    return render_template('index.html', rows = rows)

@app.route('/speed')
def getSpeed():
    route_id = request.args.get('route_id')
    if not route_id:
        route_id = 'B41'

    date = request.args.get('date')
    start_time = request.args.get('start')
    end_time = request.args.get('end')

    bus_positions_B41 = pd.read_sql(f"""
        select timestamp, trip_id, longitude, latitude from bus 
        where route_id = '{route_id}' 
    """, engine)

    bus_positions_B41['timestamp'] = pd.to_datetime(bus_positions_B41['timestamp'])


    return jsonify(bus_positions_B41.to_dict(orient = 'records'))

if __name__ == '__main__':
    setup(engine)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)