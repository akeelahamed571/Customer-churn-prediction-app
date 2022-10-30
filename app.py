# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cSOkn5QkgQgseNf-SCLoQAtf3NCbfJpv
"""

# coding: utf-8
from sklearn import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn import metrics
from flask import Flask, request, render_template
import pickle

app = Flask("__name__")
#/content/drive/MyDrive/Test/WA_Fn-UseC_-Telco-Customer-Churn.csv
file="WA_Fn-UseC_-Telco-Customer-Churn.csv"
file2="telco_new_churn.csv"

df_1=pd.read_csv(file)
col=df_1['tenure']

df_2=pd.read_csv(file2)

df_2=df_2.drop("Unnamed: 0",axis=1)

q = ""


@app.route("/")
def loadPage():
	return render_template("home.html")


@app.route("/sub",methods=["POST"])
def submit():
  if request.method=="POST":

    
    inputQuery1 = request.form['query1']
    inputQuery2 = request.form['query2']
    inputQuery3 = request.form['query3']
    inputQuery4 = request.form['query4']
    inputQuery5 = request.form['query5']
    inputQuery6 = request.form['query6']
    inputQuery7 = request.form['query7']
    inputQuery8 = request.form['query8']
    inputQuery9 = request.form['query9']
    inputQuery10 = request.form['query10']
    inputQuery11 = request.form['query11']
    inputQuery12 = request.form['query12']
    inputQuery13 = request.form['query13']
    inputQuery14 = request.form['query14']
    inputQuery15 = request.form['query15']
    inputQuery16 = request.form['query16']
    inputQuery17 = request.form['query17']
    inputQuery18 = request.form['query18']
    inputQuery19 = request.form['query19']
  
    '''
    SeniorCitizen
    MonthlyCharges
    TotalCharges
    gender
    Partner
    Dependents
    PhoneService
    MultipleLines
    InternetService
    OnlineSecurity
    OnlineBackup
    DeviceProtection
    TechSupport
    StreamingTV
    StreamingMovies
    Contract
    PaperlessBilling
    PaymentMethod
    tenure
    '''
    
    model = pickle.load(open('customer_churn_model.sav', "rb"))

    
    data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6, inputQuery7, inputQuery8, inputQuery9, inputQuery10, inputQuery11, inputQuery12, inputQuery13, inputQuery14,  inputQuery15, inputQuery16, inputQuery17, inputQuery18, inputQuery19]]
    
    new_df = pd.DataFrame(data, columns = ['SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender',  'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure'])
    

    
    df_3 = pd.concat([df_1, new_df], ignore_index = True)
    #print(df_3)

    #new_df__dummies = pd.get_dummies(new_df[['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
         #'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
         #'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
         #'Contract', 'PaperlessBilling', 'PaymentMethod','tenure']])
    new_df__dummies = pd.get_dummies(df_3[['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
         'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
         'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
         'Contract', 'PaperlessBilling', 'PaymentMethod']])
    
    #print(new_df__dummies)
    col=df_1['tenure']
    print(col)
    col=col.append(pd.DataFrame([inputQuery19]), ignore_index = True)
    print(col)
    #new_df__dummies.loc[new_df__dummies.tail(1),(len(new_df__dummies.columns)-1)] = inputQuery19
    new_df__dummies=new_df__dummies.join(col)
    print(new_df__dummies)
    #print("tenure is: ",inputQuery19)
    
    
    #print("\n last value is: ",new_df__dummies.tail(1).tenure)
   
    
    single = model.predict(new_df__dummies.tail(1))
    probablity = model.predict_proba(new_df__dummies.tail(1))[:,1]
        
    if single==1:
            o1 = "This customer is likely to be churned!!"
            o2 = "Confidence: {}".format(probablity*100)
    else:
            o1 = "This customer is likely to continue!!"
            o2 = "Confidence: {}".format(probablity*100)    
    #o1="my selected output"
    #o2="my not selected output2"        
    return render_template('submit.html', output1=o1, output2=o2, 
                              query1 = request.form['query1'], 
                              query2 = request.form['query2'],
                              query3 = request.form['query3'],
                              query4 = request.form['query4'],
                              query5 = request.form['query5'], 
                              query6 = request.form['query6'], 
                              query7 = request.form['query7'], 
                              query8 = request.form['query8'], 
                              query9 = request.form['query9'], 
                              query10 = request.form['query10'], 
                              query11 = request.form['query11'], 
                              query12 = request.form['query12'], 
                              query13 = request.form['query13'], 
                              query14 = request.form['query14'], 
                              query15 = request.form['query15'], 
                              query16 = request.form['query16'], 
                              query17 = request.form['query17'],
                              query18 = request.form['query18'], 
                              query19 = request.form['query19'])

app.run(debug=True)



