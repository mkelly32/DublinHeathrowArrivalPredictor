import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso

from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error

Y_COLUMN = 17

#######
# IMPORTING THE DATA
#######
def import_data():
    df = pd.read_csv("flight_weather_data.csv")
    print(df.head())

    Xs = []
    for i in range(0,Y_COLUMN):
        Xs.append(df.iloc[: ,i])

    # X is the list of feature vectors
    # y is the true result
    X = np.column_stack((Xs[0], Xs[1], Xs[2], Xs[3], Xs[4], Xs[5], Xs[6], Xs[7],
                        Xs[8], Xs[9], Xs[10], Xs[11], Xs[12], Xs[13], Xs[14],
                        Xs[15], Xs[16], Xs[17], Xs[18], Xs[19], Xs[20]))
    y = df.iloc[: ,Y_COLUMN]


#######
# RUNNING IT THROUGH A BASELINE MODEL
# 
# We use the mean result as the baseline regressor
#######

baseline_model = DummyRegressor(strategy="mean").fit(X, y)

# test the model and evaluate the predictions
y_pred = baseline_model.predict(X)
print("Baseline mean squared error: " + str(mean_squared_error(y,y_pred)))

#######
# RUNNING IT THROUGH A LINEAR REGRESSION MODEL
#######

linear_model = LinearRegression().fit(X, y)
y_pred = linear_model.predict(X)
print("Linear model's mean squared error: " + str(mean_squared_error(y,y_pred)))

#######
# RUNNING IT THROUGH A LASSO REGRESSION MODEL
#######

lasso_model = Lasso().fit(X, y)
y_pred = lasso_model.predict(X)
print("Lasso model's mean squared error: " + str(mean_squared_error(y,y_pred)))

#######
# 2D PLOTTING THE RESULTS
#######
plt.rc('font', size=18)
plt.rcParams['figure.constrained_layout.use'] = True
#plt.xlabel('Dublin rainfall (mm/h)'); plt.ylabel('Delay') (remember to change X[2] to X[1])
plt.xlabel('Dublin windspeed (knots)'); plt.ylabel('Delay') 

plt.rcParams["scatter.marker"] = '+'
plt.scatter(X[:,2], y_pred, color='green')
plt.rcParams["scatter.marker"] = 'o'
plt.scatter(X[:,2], y, color='blue')

plt.legend(["Prediction","True value"])
plt.show()


#######
# 3D PLOTTING THE RESULTS
#######

fig = plt.figure()
ax = fig.add_subplot(111, projection ='3d')
ax.scatter(X[:, 1], X[:, 2], y)
ax.scatter(X[:, 1], X[:, 2], y_pred)
ax.set_xlabel('Dublin rainfall (mm/h)')
ax.set_ylabel('Dublin windspeed (knots)')
ax.set_zlabel('Delay')

plt.show()