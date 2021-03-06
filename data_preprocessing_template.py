# Google Practicum

# Data Preprocessing

# Importing Libraries

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
    
# Importing dataset

Dataset = pd.read_csv('weather_data_example.csv')
X = Dataset.iloc[:,:].values
#Y = Dataset.iloc[:,3].values

# Taking care of missing data.

#from sklearn.preprocessing import Imputer
#imputer = Imputer(missing_values='NaN', strategy = 'mean', axis = 0,)
#imputer = imputer.fit(X[:,1:25]) # Not 2 instead of 3 as the uper bound is excluded.
#X[:,1:25] = imputer.transform(X[:,1:25])

# Encoding Categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[:,1:3] = labelencoder_X.fit_transform(X[:,1:3]) 
onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()
#labelencoder_Y = LabelEncoder()
#Y = labelencoder_Y.fit_transform(Y) 

# Splitting the dataset into test set and training set
#from sklearn.cross_validation import train_test_split
#X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = 0.2, random_state = 0)

# Feature Scalling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
#X_train = sc_X.fit_transform(X_train)
#X_test = sc_X.transform(X_test)
X = sc_X.transform(X)
