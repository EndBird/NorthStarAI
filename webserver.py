import os

from flask import Flask, request, jsonify, render_template
from flask_cors import cross_origin
import pandas
import pickle
import psycopg2

from sklearn.preprocessing import RobustScaler
DATABASE_URL="postgres://wfbuebdbcgdhhp:80e1efd073c910df429618085408516bf81d7468cec0eeab41af299b46b37838@ec2-23-21-248-1.compute-1.amazonaws.com:5432/d5kcgmjupq5eet"
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

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
       preds = model.predict(data)
       data['Class'] = preds
       data.to_sql('claimsreport', con=conn,  if_exists='append')

    return "Upload Successful";



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(host = '0.0.0.0', port=port)