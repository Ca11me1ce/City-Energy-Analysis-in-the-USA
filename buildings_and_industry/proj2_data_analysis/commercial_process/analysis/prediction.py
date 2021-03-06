# T-test
# Linear Regression
# Classfiers

import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from scipy import stats


def readData(file_name):
    df=pd.read_csv(file_name, sep=',')
    return df

def openFile(file_name):
    f=open(file_name, 'w')
    return f

def runKNN(X_train, Y_train, X_validate, Y_validate, num_instances):
    print('KNN in Validate Data: ')
    # f.write('\nKNN in Validate Data: \n')
    
    # Make predictions on validation dataset
    cart=KNeighborsClassifier()
    cart.fit(X_train, Y_train)

    # Get the predictions of validate data
    predictions=cart.predict(X_validate)   

    # Analyze and evaluate the predictions and models
    accu_score=accuracy_score(Y_validate, predictions)
    print(accu_score)
    # f.write('Accuracy score: '+ str(accu_score)+'\n')

    con_matrix=confusion_matrix(Y_validate, predictions)
    print(con_matrix)
    # f.write('Confusion Matrix: \n'+ str(con_matrix)+'\n')

    class_report=classification_report(Y_validate, predictions)
    print(class_report)
    # f.write('Classification Report: \n'+ str(class_report)+'\n')

def runCart(X_train, Y_train, X_validate, Y_validate, num_instances):
    # f.write('\nCart in Validate Data: \n')
    print('Cart in Validate Data: ')
    
    # Make predictions on validation dataset
    cart=DecisionTreeClassifier()
    cart.fit(X_train, Y_train)

    # Get the predictions of validate data
    predictions=cart.predict(X_validate)   

    # Analyze and evaluate the predictions and models
    accu_score=accuracy_score(Y_validate, predictions)
    print(accu_score)
    # f.write('Accuracy score: '+ str(accu_score)+'\n')

    con_matrix=confusion_matrix(Y_validate, predictions)
    print(con_matrix)
    # f.write('Confusion Matrix: \n'+ str(con_matrix)+'\n')

    class_report=classification_report(Y_validate, predictions)
    print(class_report)
    # f.write('Classification Report: \n'+ str(class_report)+'\n')

def runNB(X_train, Y_train, X_validate, Y_validate, num_instances):
    # f.write('\nNaive Bayes in Validate Data: \n')
    print('Naive Bayes in Validate Data: ')

    # Make predictions on validation dataset
    nb=GaussianNB()    # model
    nb.fit(X_train, Y_train)

    # Get the predictions of validate data
    predictions=nb.predict(X_validate)   

    # Analyze and evaluate the predictions and models
    accu_score=accuracy_score(Y_validate, predictions)
    print(accu_score)
    # f.write('Accuracy score: '+ str(accu_score)+'\n')

    con_matrix=confusion_matrix(Y_validate, predictions)
    print(con_matrix)
    # f.write('Confusion Matrix: \n'+ str(con_matrix)+'\n')

    class_report=classification_report(Y_validate, predictions)
    print(class_report)
    # f.write('Classification Report: \n'+ str(class_report)+'\n')

def runSVM(X_train, Y_train, X_validate, Y_validate, num_instances):
    # f.write('\nSVC in Validate Data: \n')
    print('SVM in Validate Data: ')
    
    # Make predictions on validation dataset
    _svc=SVC(gamma='scale')
    _svc.fit(X_train, Y_train)

    # Get the predictions of validate data
    predictions=_svc.predict(X_validate)   

    # Analyze and evaluate the predictions and models
    accu_score=accuracy_score(Y_validate, predictions)
    print(accu_score)
    # f.write('Accuracy score: '+ str(accu_score)+'\n')

    con_matrix=confusion_matrix(Y_validate, predictions)
    print(con_matrix)
    # f.write('Confusion Matrix: \n'+ str(con_matrix)+'\n')

    class_report=classification_report(Y_validate, predictions)
    print(class_report)
    # f.write('Classification Report: \n'+ str(class_report)+'\n')

def runRandomForest(X_train, Y_train, X_validate, Y_validate, num_instances):
    # f.write('\nRandom Forest in Validate Data: \n')
    print('Random Forest in Validate Data: ')
    
    # Make predictions on validation dataset
    cart=RandomForestClassifier(n_estimators=10)
    cart.fit(X_train, Y_train)

    # Get the predictions of validate data
    predictions=cart.predict(X_validate)   

    # Analyze and evaluate the predictions and models
    accu_score=accuracy_score(Y_validate, predictions)
    print(accu_score)
    # f.write('Accuracy score: '+ str(accu_score)+'\n')

    con_matrix=confusion_matrix(Y_validate, predictions)
    print(con_matrix)
    # f.write('Confusion Matrix: \n'+ str(con_matrix)+'\n')

    class_report=classification_report(Y_validate, predictions)
    print(class_report)
    # f.write('Classification Report: \n'+ str(class_report)+'\n')

def predictByClassfiers(myData):
    # Separate training and final validation data set. First remove class
    # label from data (X). Setup target class (Y)
    # Then make the validation set 20% of the entire
    # set of labeled data (X_validate, Y_validate)
    valueArray=myData.values
    X=valueArray[:, 0:5]
    Y=valueArray[:, 5]
    test_size=0.20
    seed=7
    X_train, X_validate, Y_train, Y_validate=train_test_split(X, Y, test_size=test_size, random_state=seed)

    # Setup 10-fold cross validation to estimate the accuracy of different models
    # Split data into 10 parts
    # Test options and evaluation metric
    num_folds=10
    num_instances=len(X_train)
    seed=7
    scoring='accuracy'

    ######################################################
    # Use different algorithms to build models
    ######################################################

    # Add each algorithm and its name to the model array
    models=[]
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('Naive Bayes', GaussianNB()))
    models.append(('SVM', SVC(gamma='scale')))
    models.append(('Random Forest', RandomForestClassifier(n_estimators=10)))

    # Evaluate each model, add results to a results array,
    # Print the accuracy results (remember these are averages and std
    results=[]
    names=[]
    for name, model in models:
        kfold=KFold(n_splits=num_folds, random_state=seed, shuffle=False)
        cv_results=cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg="%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)

    runKNN(X_train, Y_train, X_validate, Y_validate, num_instances)
    runCart(X_train, Y_train, X_validate, Y_validate, num_instances)
    runNB(X_train, Y_train, X_validate, Y_validate, num_instances)
    runSVM(X_train, Y_train, X_validate, Y_validate, num_instances)
    runRandomForest(X_train, Y_train, X_validate, Y_validate, num_instances)
   
def linearRegression(myData):
    valueArray=myData.values
    j=1
    for i in range(5):
        X=valueArray[:, i:j]
        Y=valueArray[:, 5]

        linear_regressor=LinearRegression()  # create object for the class
        linear_regressor.fit(X, Y)  # perform linear regression
        Y_pred=linear_regressor.predict(X)  # make predictions
        j=j+1
        # print(Y_pred)
        # print(len(X[0]))

        plt.scatter(X, Y)
        plt.plot(X, Y_pred, color='red')
        plt.show()
        plt.clf()

def tTest(myData):
    result = stats.ttest_ind(myData['elec_bin_group'], myData['gas_bin_group'])
    print("The result of t-test is: ", result)
    print("The p-valie is greater than 0.05? ", result.pvalue > 0.05)


if __name__ == "__main__":

    print('Running Linear Regression, T-test, and Classfiers')
    # Read data
    df=readData('cleaned_energy_commercial.csv')

    # Elec data
    x=[0, 1, 3, 7, 8, 10, 12]
    elec_df=df.drop(df.columns[x], axis=1)
    # print(elec_df.info())

    # Gas data
    y=[0, 1, 2, 5, 6, 9, 11]
    gas_df=df.drop(df.columns[y], axis=1)
    # print(gas_df.info())

    # Linear regression
    linearRegression(elec_df)
    linearRegression(gas_df)

    # T-test
    tTest(df)

    # Classfiers
    print('\nClassfier for Elec Dataframe: ')
    predictByClassfiers(elec_df)
    print('\nClassfier for Gas Dataframe: ')
    predictByClassfiers(gas_df)

    
    

    