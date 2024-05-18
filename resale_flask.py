# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 01:23:56 2022

@author: vkedu
"""

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
import requests
import json
from datetime import datetime
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

app = Flask('_name_',template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/y_predict', methods=['GET', 'POST'])
def y_predict():
    print(request.args.get('date'))
    la=request.args.get('Lattitude') 
    lo=request.args.get('Longtitude')
    db=datetime.strptime(request.args.get('date'), '%Y-%m-%d').toordinal()
    
    saved_model = load_model('model_1000.h5')

    # Step 1: Data Preprocessing
    data = pd.read_csv('FMD.csv')

    # Drop rows with missing values
    data.dropna(inplace=True)

    # Convert date to datetime
    data['lit_date'] = pd.to_datetime(data['lit_date'])

    # Convert date to ordinal
    data['lit_date'] = data['lit_date'].apply(lambda x: x.toordinal())

    # Split data into features and target
    X = data[['longitude', 'latitude', 'lit_date']]
    y = data['final_value']

    # Standardize numerical features
    scaler = StandardScaler()
    X[['longitude', 'latitude', 'lit_date']] = scaler.fit_transform(X[['longitude', 'latitude', 'lit_date']])

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Example prediction
    new_data = np.array([[lo, la, db]])
    scaled_data = scaler.transform(new_data)
    p = saved_model.predict(scaled_data.reshape((-1, X_train.shape[1], 1)))
    print(p[0])

    # Load the model
    loaded_model = joblib.load('manpower_RF_model.pkl')

    # Make predictions
    pm = loaded_model.predict([[la, lo]])
    print("Predicted manpower:", int(pm[0]))
    f=int(p[0])//int(pm[0]*100)
    print(p[0])
    return render_template('predict.html',msg = 'The predicted Garbage values is {:.2f} items/km and the predicted Manpower to clean is {}'.format(int(p[0])**(0.5),f))
    #return "Successfully completed"
app.run(debug=True)