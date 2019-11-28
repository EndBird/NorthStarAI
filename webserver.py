import os

from flask import Flask, request, jsonify, render_template
from flask_cors import cross_origin
import pandas
import pickle

from sklearn.preprocessing import RobustScaler

model = pickle.load(open('LogisiticRegression.sav', 'rb'))

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
@cross_origin()
def upload():
    if request.method == 'POST':

       file = request.files['Upload']
       data = pandas.read_csv(file)
       rob_scaler = RobustScaler()
       data = data.drop('Class', axis=1)
       data['Amount'] = rob_scaler.fit_transform(data['Amount'].values.reshape(-1, 1))
       data['Time'] = rob_scaler.fit_transform(data['Time'].values.reshape(-1, 1))
       #for some reason scaling is required for non frauds but for fraud no scaling
       model.predict(data)

    return "Upload Successful";



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(host = '0.0.0.0', port=port)