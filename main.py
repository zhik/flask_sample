from flask import Flask, send_file, render_template, jsonify
import pandas as pd

df = pd.read_csv('2023-05-17-bus-positions_1.csv')
df = df.dropna(subset = 'route_id')

app = Flask(__name__, template_folder='templates')

@app.route('/<bus_route>')
def greeting(bus_route):
    df2 = df[df['route_id'].str.contains(bus_route)]
    return jsonify(df2.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)

