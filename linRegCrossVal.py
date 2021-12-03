#######
# RESULTS
#
# 
#
#
#
#
#######


#######
# IMPORTS
#######
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.dummy import DummyRegressor

from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score

Y_COLUMN = 21

#######
# IMPORTING THE DATA
#######
def import_data():
    df = pd.read_csv("flight_weather_data.csv")
    print(df.head())

    Xs = []
    for i in range(0,Y_COLUMN):
        Xs.append(df.iloc[: ,i])

    # experimental - wighting the wind by its direction, such that
    # a direction towards london leaves it the same, away from london
    # is equal but negative, and sideways is discarded. Bearing from
    # DUB to LON is 111 degrees
    newXs1 = []
    newXs2 = []
    for i in range(0,len(Xs[0])):
        newXs1.append((((1 - (abs(111 - Xs[3][i]) / 180)) * 2) - 1) * Xs[2][i])
        newXs2.append((((1 - (abs(111 - Xs[9][i]) / 180)) * 2) - 1) * Xs[8][i])
    Xs[2] = newXs1
    Xs[8] = newXs2

    # X is the list of feature vectors
    # y is the true result
    X = np.column_stack((Xs[2], Xs[4], Xs[5],
                        Xs[8], Xs[10], Xs[11]))
    
    # X is the list of feature vectors
    # y is the true result
    """ X = np.column_stack((Xs[0], Xs[1], Xs[2], Xs[3], Xs[4], Xs[5], Xs[6], Xs[7],
                        Xs[8], Xs[9], Xs[10], Xs[11], Xs[12], Xs[13], Xs[14],
                        Xs[15], Xs[16], Xs[17], Xs[18], Xs[19], Xs[20])) """
    
    # This picks only the wind related features (still no benefit compared to baseline)
    """ X = np.column_stack((Xs[3], Xs[4], Xs[5],
                        Xs[8], Xs[9], Xs[10])) """
    y = df.iloc[: ,Y_COLUMN]
    #print(y)
    #print(X[0])
    return [X,y]
    
#######
# CROSS VALIDATION
#
# Only applies where there are hyperparameters (ie. Lasso, Ridge, KNN...)
#
# We get a ConvergenceWarning (can be sort of fixed with higher iterations or
# higher tol), however it is a bad sign indicating possible overfitting, in this
# case as a result of the polynomial features.
#
# The reason the cross validate returns negative mean_squared_error is because the return
# type can be set to scores or accuracy measures, and by keeping scores negative, then for
# both, higher = better
#
# Use ANSI escape sequences to underline subtitle
#
# alpha = 1/2C  -  C = 0.01 -> alpha = 50  -  C = 1 -> alpha = 0.5  -  C = 100 -> 0.005
#######
def Xval(X, y, model, independant_vars, polyCount):
    mean_error=[]
    std_error=[]
    meanbase_error=[]
    stdbase_error=[]
    
    plt.clf()
    for independant_var in independant_vars:
        # Select model
        if  (model == "lasso"):
            selectedModel = Lasso(alpha=independant_var).fit(X, y)
            plt.xlabel('C')
        elif(model == "ridge"):
            selectedModel = Ridge(alpha=independant_var).fit(X, y)
            plt.xlabel('C')
        #elif(model == "linear"):
        #    selectedModel = LinearRegression().fit(X, y)
        elif(model == "knn"):
            selectedModel = KNeighborsRegressor(n_neighbors=independant_var, weights='uniform').fit(X, y)
            plt.xlabel('# of neighbours')
            
        # Run model
        scores = cross_val_score(selectedModel, X, y, cv=5, scoring='neg_mean_squared_error')
        scores = scores * -1
        print(str(independant_var) + ": " + str(scores * (-1)))
        print("Avg: " + str(sum(scores)/len(scores)))
        mean_error.append(np.array(scores).mean())
        std_error.append(np.array(scores).std())
        
        # Run baseline model
        baseModel =  DummyRegressor(strategy="mean")
        scores = cross_val_score(baseModel, X, y, cv=5, scoring='neg_mean_squared_error')
        scores = scores * -1
        meanbase_error.append(np.array(scores).mean())
        stdbase_error.append(np.array(scores).std())
    
    for i in range(0,len(independant_vars)):
        independant_vars[i] = 1 / (2 * independant_vars[i])
        
    plt.title('Cross validation (cv=5) for ' + model + ' model with poly: '+ str(polyCount))
    plt.errorbar(independant_vars,mean_error,yerr=std_error,linewidth=3)
    plt.errorbar(independant_vars,meanbase_error,yerr=stdbase_error)
    plt.ylabel('Mean Squared Error')
    plt.xscale('log')
    plt.legend(["model predictions", "baseline predictions"])
    # plt.show()
    plt.savefig('CV_' + model + '-poly_' + str(polyCount) + '.png')

#def XvalLinear(X, y):
#    print('\033[4m' + "Ridge mean_squared_error scores" + '\033[0m')
#    alphas = [5000, 500, 50, 5, 0.5, 0.05, 0.005]
#    Xval(X, y, "linear", alphas)

def XvalLasso(X, y, polyCount):
    print('\033[4m' + "Lasso mean_squared_error scores" + '\033[0m')
    alphas = [5000, 500, 50, 5, 0.5, 0.05, 0.005]
    Xval(X, y, "lasso", alphas, polyCount)

def XvalRidge(X, y, polyCount):
    print('\033[4m' + "Ridge mean_squared_error scores" + '\033[0m')
    alphas = [5000, 500, 50, 5, 0.5, 0.05, 0.005]
    Xval(X, y, "ridge", alphas, polyCount)

def XvalKNN(X, y, polyCount):
    print('\033[4m' + "KNN mean_squared_error scores" + '\033[0m')
    num_of_neighbours = [100, 50, 10, 5, 1]
    Xval(X, y, "knn", num_of_neighbours, polyCount)

################
########### MAIN
###########
########### When we vary poly features between 1:4 the results get
########### significantly worse, so we leave it at 1.
###########
########### All the models seem to do WORSE than the baseline
################
[X,y] = import_data()

polyRange = range(1,3)
for cPoly in polyRange:
    poly = PolynomialFeatures(cPoly)
    powerFeatures = poly.fit_transform(X)
    # XvalLasso(powerFeatures, y, cPoly) 
    # XvalRidge(powerFeatures, y, cPoly)     
    XvalKNN(powerFeatures, y, cPoly)