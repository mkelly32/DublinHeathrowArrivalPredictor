import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

Y_COLUMN = 17

# Importing the data
df = pd.read_csv("flight_weather_data.csv")
print(df.head())

Xs = []
for i in range(0,Y_COLUMN):
    Xs.append(df.iloc[: ,i])
    
X = np.column_stack((Xs[0], Xs[1], Xs[2], Xs[3], Xs[4], Xs[5], Xs[6], Xs[7],
                     Xs[8], Xs[9], Xs[10], Xs[11], Xs[12], Xs[13], Xs[14],
                     Xs[15], Xs[16]))
y = df.iloc[: ,Y_COLUMN]

#print(y)
#print(X[0])