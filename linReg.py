import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor

from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error



#######
# IMPORTING THE DATA
#######
Y_COLUMN = 21

df = pd.read_csv("flight_weather_data.csv")
print(df.head())

Xs = []
for i in range(0,Y_COLUMN):
    Xs.append(df.iloc[: ,i])
    
# experimental - wighting the wind by its direction, such that
# a direction towards london leaves it the same, away from london
# is equal but negative, and sideways is discarded. Bearing from
# DUB to LON is 111 degrees
""" newXs1 = []
newXs2 = []
for i in range(0,len(Xs[0])):
    newXs1.append((((1 - (abs(111 - Xs[3][i]) / 180)) * 2) - 1) * Xs[2][i])
    newXs2.append((((1 - (abs(111 - Xs[9][i]) / 180)) * 2) - 1) * Xs[8][i])
Xs[2] = newXs1
Xs[8] = newXs2 """

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

""" baseline_model = DummyRegressor(strategy="mean").fit(X, y)

# test the model and evaluate the predictions
y_pred = baseline_model.predict(X)
print("Baseline mean squared error: " + str(mean_squared_error(y,y_pred))) """

#######
# RUNNING IT THROUGH A LINEAR REGRESSION MODEL
#
# No hyperparameter here, so no CV necessary
#######

""" linear_model = LinearRegression().fit(X, y)
y_pred = linear_model.predict(X)
print("Linear model's mean squared error: " + str(mean_squared_error(y,y_pred))) """

#######
# RUNNING IT THROUGH A RIDGE REGRESSION MODEL
#
# The best score where poly=1 was for alpha = 50, sum([  -86.06456327 
# -1162.46284228 -182.62735806   -21.68576525 -71.87161024])/5 = -304.94242782000003
# This was a better result than any provided by poly=2, where sum([-2522.71345719 
# -1172.27372331  -275.30982059   -44.52428217 -314.67916562])/5 = -865.9000897760001
# Thus we choose poly=1 with alpha=50
#######

""" ridge_model = Ridge(alpha=50).fit(X, y)
y_pred = ridge_model.predict(X)
print('intercept', ridge_model.intercept_, ' slope', ridge_model.coef_)
print("Ridge model's mean squared error: " + str(mean_squared_error(y,y_pred))) """

#######
# RUNNING IT THROUGH A LASSO REGRESSION MODEL
# From the plots we can see that alpha larger than 50 performs best, and
# by looking at the individual scores we see that for alpha = 500 or 5000, the
# results are exactly the same.
# Comparing the best score of poly=1 and poly=2 gives us, we see poly=1 gives us
# the better result: sum([  -36.30367944 -1161.43222968  -175.02720531
# -17.67862189 -69.24844292])/5 = -291.93803584799997, than poly=2: 
# sum([  -60.73180791 -1162.3313063   -175.18044385   -16.40347565 -71.05432283])/5 
# = -297.140271308
# Thus we chose poly=1 and alpha=500.
#
# HOWEVER, we can learn a lot about the features have the most impact according to the
# model, by setting alpha low (acknowledging that this gives worse results than the baseline)
# params: [ 0.22518315   -0.          0.          0.00434525  0.          0. -0.03431487  
# 0.          0.04214754 -0.00455631 -0.04291345 -0.  0.          0.          0.         
# 0.         -0.          0. -0.         -0.         -0.        ]
#######

lasso_model = Lasso(alpha=1).fit(X, y)
y_pred = lasso_model.predict(X)
print('intercept', lasso_model.intercept_, ' slope', lasso_model.coef_)
print("Lasso model's mean squared error: " + str(mean_squared_error(y,y_pred)))

#######
# RUNNING IT THROUGH A KNN REGRESSION MODEL
#
# The plot of poly=1 and poly=2 shows that #Neighbours=100 
# performs best, with an average of sum([  -49.17778333 -1161.48342778  
# -181.35708519   -20.74891019 -74.97579252])/5 = -297.548599802 for
# poly=1 and sum([  -52.13356759 -1165.45733519  -181.1228037    
# -19.00404722 -73.30196355])/5 = -298.20394345000005 for poly=2
# Thus we choose poly=1 with #=100
#######

""" knn_model = KNeighborsRegressor(n_neighbors=100, weights='uniform').fit(X, y)
y_pred = knn_model.predict(X)
print('intercept', knn_model.intercept_, ' slope', knn_model.coef_)
print("KNN model's mean squared error: " + str(mean_squared_error(y,y_pred))) """


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