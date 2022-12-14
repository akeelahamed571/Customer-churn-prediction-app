# -*- coding: utf-8 -*-
"""FDM_project_practise.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GYm-TzrnGuMrUXyQUYdPmFdQDOmqN4Ln
"""

from google.colab import drive
drive.mount("/content/drive/",force_remount=False)

"""# **data anlaysis and cleansing**"""

# import data seta 
file="/content/drive/MyDrive/Test/WA_Fn-UseC_-Telco-Customer-Churn.csv"
import pandas as pd
import matplotlib.pyplot as plt

missing_values = ["n/a", "na", "--"," "]
#df=pd.read_csv(file,na_values=missing_values)
df=pd.read_csv(file)

df.head()

"""**data description**"""

df.shape

df.describe()

df.dtypes

"""**we noticed totalcharges is in obj data type but we need that as float**
---


---


"""

# convert to numeric
df.TotalCharges=pd.to_numeric(df.TotalCharges,errors='coerce')

df.isnull().sum()

df.dtypes

#location of null values
df.loc[df["TotalCharges"].isnull()==True]

#outliers checking before fill up null values
import seaborn as sys
sys.boxplot(df['TotalCharges'])

sys.boxplot(df['MonthlyCharges'])

"""**since are no outliers in Total Charges we don't need to remove any values and we can fill null values with the median** """

#fill null values
median=df['TotalCharges'].median()

df['TotalCharges'].fillna(median, inplace=True)

df.isnull().sum()

#remove columns

df.drop(columns= ['customerID'], axis=1, inplace=True)

#visulaize count of churn and not churn for each independent variable
#please wait for few mins until it loads all graphs and charts
import seaborn as sys

for i in (df):
  
    plt.figure(i)
    sys.catplot(data=df,x=i,hue='Churn',kind='count',palette="ch:.35")

# plotting correlation heatmap
dataplot = sys.heatmap(df.corr(), cmap="YlGnBu", annot=True)
plt.show()

df

import numpy  as np
df['Churn'] = np.where(df.Churn == 'Yes',1,0)
df

df['Churn']

#dummy the dataframe to convert categorical variables into numerical variables for further analysis 
df_dummy = pd.get_dummies(df)

df_dummy

#dataplot=sys.heatmap(df_dummy.corr())
#plt.show()

# correlation with churn column plotting for each and every variable in dummy df
plt.figure(figsize=(20,10))
df_dummy.corr()['Churn'].sort_values(ascending = False).plot(kind='bar')

#numerically represents correlation with churn class attribute
df_dummy.corr()['Churn'].sort_values(ascending = False)



"""HIGH Churn seen in case of Month to month contracts, No online security, No Tech support, and Fibre Optics Internet

LOW Churn is seens in case of  Subscriptions without internet service ,long term contract

[TechSupport_No                             0.337281
InternetService_Fiber optic                0.308020
PaymentMethod_Electronic check             0.301919
OnlineBackup_No                            0.268005]

Factors like Gender, Availability of PhoneService and # of multiple lines have alomost NO impact on Churn
"""

df_dummy.to_csv('telco_new_churn.csv')



"""
### **preparing dataset further more by reading preprocessed dataset,spliting into features,target and split to train ,test**"""

import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from imblearn.combine import SMOTEENN

df_model=pd.read_csv("/content/telco_new_churn.csv")

df_model=df_model.drop("Unnamed: 0",axis=1)

x_values=df_model.drop("Churn",axis=1)

y_value=df_model["Churn"]
y_value

x_train,x_test,y_train,y_test=train_test_split(x_values,y_value,test_size=0.2)

# checking how many churn and non churned customes are there
y_value.value_counts().plot(kind='bar',figsize=(8,6))
plt.xlabel("churn values")
plt.ylabel("count")
plt.title("churn column")

#checking balance of data set
100* y_value.value_counts()/len(y_value)

"""**data set is too imbalanced now we need to balanace it .so we can use SMOTEENN which SMOTE+ENN method of combining oversampling with under sampling**

## **Resampling using SMOTEENN**
"""

sm = SMOTEENN()
#from imblearn.over_sampling import SMOTE
#sm=SMOTE()
X_resampled, y_resampled = sm.fit_resample(x_values,y_value)

#checking rebalanced data percentage of churn class
100* y_resampled.value_counts()/len(y_resampled)

"""# **Model Build**

##**Decision tree**
"""

model_dt=DecisionTreeClassifier(criterion = "gini",random_state=0  )

# random_state = 100,max_depth=6, min_samples_leaf=8

model_dt.fit(x_train,y_train)

y_pred=model_dt.predict(x_test)
y_pred

model_dt.score(x_test,y_test)

print(classification_report(y_test, y_pred))

"""**here even though we had 79% accuracy still our minority class f1 score recall precision still very low because of imbalanced data set.now let's rebalance the data set using upsampling + down sampling technique(SMOTEENN)**

**building decision tree classifier using rebalanced datset**
"""

xr_train,xr_test,yr_train,yr_test=train_test_split(X_resampled, y_resampled,test_size=0.2)

model_resampled_dt=DecisionTreeClassifier(criterion = "gini",random_state=0  )

model_resampled_dt.fit(xr_train,yr_train)

y_prediction_resampled_dt=model_resampled_dt.predict(xr_test)

model_resampled_dt.score(xr_test,yr_test)

"""**92.9% accuracy**"""

print(classification_report(yr_test,y_prediction_resampled_dt))

confusion_matrix(yr_test,y_prediction_resampled_dt)

"""##**RandomForest classify**"""

from sklearn.ensemble import RandomForestClassifier

random_forest_model=RandomForestClassifier()
random_forest_model.fit(x_train,y_train)
y_predict_value_random_forest=random_forest_model.predict(x_test)

random_forest_model.score(x_test,y_test)

print(classification_report(y_test,y_predict_value_random_forest))



"""**here even though we had 79% accuracy still our minority class f1 score recall precision still very low because of imbalanced data set.now let's rebalance the data set using upsampling + down sampling technique(SMOTEENN)**

**here below we don't need to re implement SMOTEEN() because we already implemented SMOTEEN() and rebalanced  dataset in data analysis.so we can use that dataset here.**
"""

100* y_resampled.value_counts()/len(y_resampled)

model_rf_resampled=RandomForestClassifier()
model_rf_resampled.fit(xr_train,yr_train)
model_rf_resampled.score(xr_test,yr_test)

"""**95.5%**"""

yr_rf_predicted_values=model_rf_resampled.predict(xr_test)

print(classification_report(yr_test,yr_rf_predicted_values))

confusion_matrix(yr_test,yr_rf_predicted_values)



"""##**Logistic Regression**"""

from sklearn.linear_model import LogisticRegression

model_lr=LogisticRegression(solver='lbfgs', max_iter=1000)
model_lr.fit(x_train,y_train)

y_lr_predicted_value=model_lr.predict(x_test)

model_lr.score(x_test,y_test)

y_lr_predicted=model_lr.predict(x_test)
print(classification_report(y_test,y_lr_predicted))



"""**here even though we had 81% accuracy still our minority class f1 score recall precision still very low because of imbalanced data set.now let's rebalance the data set using upsampling + down sampling technique(SMOTEENN)**

**here below we don't need to re implement SMOTEEN() because we already implemented SMOTEEN() and realanced teh dataset in decision tree classifier.so we can use that dataset here.**
"""

#xr_lr_train,xr_lr_test,yr_lr_train,yr_lr_test=train_test_split(xr_lr_values,yr_lr_value)
model_lr_resampled=LogisticRegression(solver='lbfgs',max_iter=10000)

model_lr_resampled.fit(xr_train,yr_train)
model_lr_resampled.score(xr_test,yr_test)

"""**94.8%**"""

yr_lr_predicted_value=model_lr_resampled.predict(xr_test)
print(classification_report(yr_test,yr_lr_predicted_value))

confusion_matrix(yr_test,yr_lr_predicted_value)

"""
##**XGBooost (gradient boost)**"""

from xgboost import XGBClassifier

model_xgb=XGBClassifier(use_label_encoder=False,eval_metrics='mlogloss')
model_xgb.fit(x_values,y_value)
model_xgb.score(x_test,y_test)

y_xgb_predicted_value=model_xgb.predict(x_test)

print(classification_report(y_test,y_xgb_predicted_value))

"""**even though accuracy is 83% ,customer churn class(1) has low f1 score ,precision,accuracy.so we use SMOTEEN technique to rebalance the data set**

**here below we don't need to re implement SMOTEEN() because we already implemented SMOTEEN() and realanced teh dataset in decision tree classifier.so we can use that dataset here.**
"""

model_xgb_resampled=XGBClassifier(use_label_encoder=False,eval_metrics='mlogloss')

model_xgb_resampled.fit(xr_train,yr_train)
yr_xgb_predicted_val=model_xgb_resampled.predict(xr_test)
model_xgb_resampled.score(xr_test,yr_test)

"""**95.2%**"""

print(classification_report(yr_test,yr_xgb_predicted_val))

metrics.accuracy_score(yr_test,yr_xgb_predicted_val)

confusion_matrix(yr_test,yr_xgb_predicted_val)

"""# **Finally we will Choose an algorithm for the model based on high accuracy**

## **and it is from random forest  and 95.5% accuracy.now we save the model using pickle and load**
"""

import pickle

pickle.dump(model_rf_resampled, open('customer_churn_model.sav', 'wb'))

pickled_model = pickle.load(open('customer_churn_model.sav', 'rb'))

pickled_model.score(xr_test,yr_test)





"""# UI UX"""