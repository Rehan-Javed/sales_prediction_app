from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import pandas as pd
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('finalized_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Influencer__Macro = 1
    Influencer__Mega = 0
    Influencer__Micro = 0
    Influencer__Nano = 0

    if request.method == 'POST':
        TV = float(request.form['TV'])
        Radio = float(request.form['Radio'])
        Social_Media = float(request.form['Social_Media'])

        Influencer_type = request.form['Influencer_type']
        
        if(Influencer_type=='Macro'):
            Influencer__Macro=1
            Influencer__Mega=0
            Influencer__Micro=0
            Influencer__Nano=0

        elif(Influencer_type=='Mega'):
            Influencer__Macro=0
            Influencer__Mega=1
            Influencer__Micro=0
            Influencer__Nano=0


        elif(Influencer_type=='Micro'):
            Influencer__Macro=0
            Influencer__Mega=0
            Influencer__Micro=1
            Influencer__Nano=0

        else:
            Influencer__Macro=0
            Influencer__Mega=0
            Influencer__Micro=0
            Influencer__Nano=1


        prediction=model.predict([[TV, Radio, Social_Media, 
        Influencer__Macro, Influencer__Mega, Influencer__Micro, Influencer__Nano]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry we can't predict this")
        else:
            return render_template('index.html',prediction_text="The sales you can generate is {} million".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

