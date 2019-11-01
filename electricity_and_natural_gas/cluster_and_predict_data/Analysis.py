#######################
# Author: Dandan Wang
# NetID: dw862
# Function: clean data, cluster data and predict data.
# ####################

import csv
import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score, calinski_harabasz_score
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn import decomposition
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

def extractData():
    myData = pd.read_csv("../collect_and_clean_data/cleaned_residential.csv", sep=',', encoding='latin1')
    myData.drop(['elec_1kdollars_bin_min', 'elec_1kdollars_bin_max', 'elec_mwh_bin_min', 'elec_mwh_bin_max', 'gas_1kdollars_bin_min', 'gas_1kdollars_bin_max', 'gas_mcf_bin_min', 'gas_mcf_bin_max', 'elec_min_lb_ghg', 'elec_max_lb_ghg', 'gas_min_lb_ghg', 'gas_max_lb_ghg'], axis = 1, inplace=True)
    return myData

def insertState(myData):
    df = pd.read_csv("../../population_data/processed_us_zips.csv", sep=',', encoding='latin1')
    df.drop(['Unnamed: 0', 'timezone', 'lat', 'lng', 'city','state_name', 'zcta', 'parent_zcta', 'population', 'density', 'county_fips', 'county_name', 'all_county_weights', 'imprecise', 'military', 'military'], axis = 1, inplace = True)
    myData = pd.merge(myData, df, how = 'left', on = 'zip', right_index = False)
    return (df, myData) 

def getCommonAttrs(df0):
    # Extract the useful attributes in cleaned_commercial.csv files.
    df = pd.read_csv("../collect_and_clean_data/cleaned_commercial.csv", sep=',', encoding='latin1')
    df.drop(['elec_1kdollars_bin_min', 'elec_1kdollars_bin_max', 'elec_mwh_bin_min', 'elec_mwh_bin_max', 'gas_1kdollars_bin_min', 'gas_1kdollars_bin_max', 'gas_mcf_bin_min', 'gas_mcf_bin_max', 'elec_min_lb_ghg', 'elec_max_lb_ghg', 'gas_min_lb_ghg', 'gas_max_lb_ghg'], axis = 1, inplace = True)
    df = pd.merge(df, df0, how = 'left', on = 'zip', right_index = False)
    df.drop(['zip'], axis = 1, inplace = True)
    # Drop duplicated rows and merge different rows with same state and city.
    df.drop_duplicates(inplace=True) 
    df = df.groupby(['state_id', 'city']).sum()
    df.to_csv("common_attrs_commercial.csv")
    # Extract the useful attributes in cleaned_commercial.csv files.
    df = pd.read_csv("../collect_and_clean_data/cleaned_industrial.csv", sep=',', encoding='latin1')
    df.drop(['elec_1kdollars_bin_min', 'elec_1kdollars_bin_max', 'elec_mwh_bin_min', 'elec_mwh_bin_max', 'gas_1kdollars_bin_min', 'gas_1kdollars_bin_max', 'gas_mcf_bin_min', 'gas_mcf_bin_max', 'elec_min_lb_ghg', 'elec_max_lb_ghg', 'gas_min_lb_ghg', 'gas_max_lb_ghg'], axis = 1, inplace = True)
    df = pd.merge(df, df0, how = 'left', on = 'zip', right_index = False)
    df.drop(['zip'], axis = 1, inplace = True)
    # Drop duplicated rows and merge different rows with same state and city.
    df.drop_duplicates(inplace=True)
    df = df.groupby(['state_id', 'city']).sum() 
    df.to_csv("common_attrs_industrial.csv")

def statisticalAnalysis(myData):
    attrs = ['housing_units', 'total_pop', 'elec_1kdollars', 'elec_mwh', 'gas_1kdollars', 'gas_mcf', 'elec_lb_ghg', 'gas_lb_ghg']
    mean = np.mean(myData[attrs])
    std = np.std(myData[attrs])
    print("The mean of each attribute is: \n", mean)
    print("\nThe median of each attribute is: ")
    for i in range(len(attrs)):
        print(attrs[i], "   ", np.median(myData[attrs[i]]))
    print("\nThe standard deviation of each attribute is: \n", std)

def dropDuplicate(myData):
    myData.drop(['zip'], axis = 1, inplace = True)
    # Drop all totally same rows except zip.
    myData.drop_duplicates(inplace=True)
    # Merge rows with same city and state.
    myData = myData.groupby(['state_id', 'city']).sum()
    myData.to_csv("cleaned_residential.csv")

def extractAttrs():
    # Extract useful attributes form the cleaned data.
    myData = extractData()
    # Insert the state abbreviation into the dataframe.
    (df, myData) = insertState(myData)
    # Extract the useful attributes for commercial and industrial analysis.
    # Store the extracted attributes in "common_attrs_commercial.csv" and "common_attrs_industrial.csv".
    # Then my members can directly read data from these two file.
    getCommonAttrs(df)
    # Drop duplicated rows and merge rows with the same state abbreviation and city name.
    dropDuplicate(myData)
    return myData

def binning(myData, attr, k):
    # Create even spaced bins using min and max
    minNum = myData[attr].min() - 1
    maxNum = myData[attr].max() + 1
    #print(myData['total_pop'].min())
    #print(myData['total_pop'].max())
    n_bin = k
    step = (maxNum - minNum) / n_bin
    bins =  np.arange(minNum, maxNum + step, step)
    #This is equi-width binning
    Bins = np.digitize(myData[attr], bins)
    # Count the number of values in each bin
    BinCounts = np.bincount(Bins)
    print("\nBin count of ", attr, " is ", BinCounts)
    return (BinCounts, bins)

def binOutlier(myData, attr, upperBound):
    (BinCounts, bins) = binning(myData, attr, 100)
    outlierAmount = 0
    totalAmount = 0
    for i in range(100):
        if i < 1 or i > 11:
            outlierAmount += BinCounts[i]
        totalAmount += BinCounts[i]
    print("\nOutlier percentage of ", attr, " is ", outlierAmount * 1.00 / totalAmount)
    # Store the upper bound into the upperBound list.
    upperBound.append(bins[11])

def deleteOutliers(myData, attr,upperBound):
    # To compare LOF and binning method.
    # Do not change myData directly.
    # Make a copy of precessed data frame.
    binnedData = myData[myData[attr] < upperBound]
    return binnedData

def binData(myData):
    # Save the upper bound of non-outliers.
    upperBound = []
    # The collection of attributes that might have outliers
    attrs = ['housing_units', 'total_pop', 'elec_1kdollars', 'elec_mwh', 'gas_1kdollars', 'gas_mcf', 'elec_lb_ghg', 'gas_lb_ghg']
    # For each attribute, bin it get the upper bound of non-outliers.
    for attr in attrs:
        binOutlier(myData, attr, upperBound)
    # Delete the outliers. 
    # To compare LOF and binning method. Do not change myData directly. Make a copy of myData and change it.
    for i in range(len(attrs)):
        binnedData = deleteOutliers(myData, attrs[i], upperBound[i])
    # The result is stored into file.
    binnedData.to_csv("binned_residential.csv")
    return binnedData

def findMissing(myData):
    frac = myData.isna().sum() * 1.00 / len(myData)
    print("the fraction of missing value is: ", frac)

def binClass(myData):
    (BinCounts, bins) = binning(myData, "elec_mwh", 5)
    myData["elec_degree"] = np.digitize(myData["elec_mwh"], bins)
    (BinCounts, bins) = binning(myData, "gas_mcf", 5)
    myData["gas_degree"] = np.digitize(myData["gas_mcf"], bins)
    # Store the data frame with two new attributes into a new file.
    binnedData.to_csv("degreed_residential.csv", index=False)

def LOF(myData):
    valueArray = myData.values
    X = valueArray[:, 1:9]
    # different values for k.
    k = [100, 500, 1000]
    # new attributes.
    attrs = ['lof_score_100', 'lof_score_500', 'lof_score_1000']
    # The lower bound of non-outliers.
    lowerBound = []
    # Try every k value.
    for i in range(len(k)):
        lof = LocalOutlierFactor(n_neighbors = k[i], contamination = 0.002)
        lof.fit(X)
        scores = lof.negative_outlier_factor_
        myData[attrs[i]] = scores 
        print("The k of LOF is ", k[i])
        # Using binning method to observe the distributions of lof factors.
        (BinCounts, bins) = binning(myData, attrs[i], 10)
        lowerBound.append(bins[-2])
    
    myData = myData[myData[attrs[i]] > lowerBound[i]] 
    myData.to_csv("lof_residential.csv")

def compare(myData, binnedData):
    print("For LOF algorithm:")
    binning(myData, "elec_mwh", 5)
    binning(binnedData, "gas_mcf", 5)
    print("For binning method:")
    binning(binnedData, "elec_mwh", 5)
    binning(binnedData, "gas_mcf", 5)

def plotData(binnedData):
    df = binnedData.drop(['state_id', 'city', 'elec_degree', 'gas_degree', 'elec_1kdollars', 'gas_1kdollars', 'elec_lb_ghg', 'gas_lb_ghg'], axis = 1)
    df.hist()
    #plt.savefig('Histogram.png')
    plt.show()

def correlation(binnedData):
    # Get the sub data set with 4 attributes.
    df = binnedData.drop(['state_id', 'city', 'elec_degree', 'gas_degree', 'elec_1kdollars', 'gas_1kdollars', 'elec_lb_ghg', 'gas_lb_ghg'], axis = 1)
    # Print the correlation matrix of the 4 attributes.
    print(df.corr())
    # Plot a set of scatterplot subplots.
    scatter_matrix(df)
    plt.show()
    #plt.savefig('scatterplot.png')

def clustering(binnedData):
    # Drop non-numeric attributes and degree attributes which are generated by other attributes.
    myData = binnedData.drop(['state_id', 'city', 'elec_degree', 'gas_degree'], axis = 1)
    x = myData.values
    # Normalize raw data.
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    # The list of clustering methods.
    clusteringMethod = ['k-means', 'Ward', 'DBScan']
    # To save the cluster labels of each method.
    cluster_labels = []   
    # Apply each method, and store the generated labels into cluster_labels list.
    kmeans = KMeans(n_clusters = 5)
    cluster_labels.append(kmeans.fit_predict(normalizedDataFrame))
    ward = AgglomerativeClustering(linkage = 'ward', n_clusters = 5)
    cluster_labels.append(ward.fit_predict(normalizedDataFrame))
    dbscan = DBSCAN(eps = 0.05, min_samples = 50)
    cluster_labels.append(dbscan.fit_predict(normalizedDataFrame))    
    # Determine if the clustering is good
    for i in range(len(clusteringMethod)):
        silhouette_avg = silhouette_score(normalizedDataFrame, cluster_labels[i])
        score = calinski_harabasz_score(normalizedDataFrame, cluster_labels[i])
        print("For ", clusteringMethod[i], " clustering, the average silhouette_score is :" + str(silhouette_avg) + "; the calinski harabasz score is :" + str(score) + ".")
        # Let's convert our high dimensional data to 2 dimensions
        # using PCA
        pca2D = decomposition.PCA(2)
        pca2D = pca2D.fit(normalizedDataFrame)
        plot_columns = pca2D.transform(normalizedDataFrame)
        # This shows how good the PCA performs on this dataset
        print("For ", clusteringMethod[i], "clustering, the pca score is ", pca2D.explained_variance_)
        # Plot using a scatter plot and shade by cluster label
        plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels[i])
        plt.title(clusteringMethod[i] + " pca2D")
        name = clusteringMethod[i] + "_pca2D.png"
        plt.savefig(name)
    
def associationRule(myData):
    # Extract attributes to form sub data set.
    df = myData.drop(['city', 'housing_units', 'total_pop', 'elec_mwh', 'gas_mcf', 'elec_1kdollars', 'gas_1kdollars', 'elec_lb_ghg', 'gas_lb_ghg'], axis = 1)
    # Convert the type of degree attributes to string.
    attrs = ['elec_degree', 'gas_degree']
    for attr in attrs:
        df[attr][df[attr] == 1] = attr + "_very_low"
        df[attr][df[attr] == 2] = attr + "_low"
        df[attr][df[attr] == 3] = attr + "_medium"
        df[attr][df[attr] == 4] = attr + "_high"
        df[attr][df[attr] == 5] = attr + "_very_high"
    # Apply Apriori algorithm.
    valueArray = df.values
    te = TransactionEncoder()
    te_ary = te.fit(valueArray).transform(valueArray)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    result = apriori(df, min_support=0.05, use_colnames=True) 
    #print(result.support.max())
    print(result)

def evaluateAlg(myData, k):
    # First remove class label from data (X). Setup target class (Y)
    valueArray = myData.values
    X = valueArray[:, :6]
    Y = valueArray[:, k] 
    # Then make the validation set 20% of the entire set of labeled data (X_validate, Y_validate)
    test_size = 0.20
    seed = 7

    X_train, X_validate, Y_train, Y_validate = train_test_split(X, Y, test_size=test_size, random_state=seed)
    # Setup 10-fold cross validation to estimate the accuracy of different models
    # Split data into 10 parts
    # Test options and evaluation metric
    num_folds = 10
    num_instance = len(X_train)
    seed = 7
    scoring = 'accuracy'
    # Use different algorithms to build models
    # Add each algorithm and its name to the model array
    models = []
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('DecisionTree', DecisionTreeClassifier()))
    models.append(('Naive Bayes', MultinomialNB()))
    models.append(('SVM', SVC(gamma = 'scale')))
    models.append(('RandomForest', RandomForestClassifier()))
    #Evaluate each model, add results to a results array
    # Print the accuracy results (remember these are averages and std)
    results = []
    names = []
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=False)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
    return (X_train, Y_train, X_validate, Y_validate)

def validateData(X_train, Y_train, X_validate, Y_validate):
    # For each machine learning method, see how well it does on the validation test
    models = []
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('DecisionTree', DecisionTreeClassifier()))
    models.append(('Naive Bayes', MultinomialNB()))
    models.append(('SVM', SVC(gamma = 'scale')))
    models.append(('RandomForest', RandomForestClassifier()))
    for name, model in models:
        model.fit(X_train, Y_train)
        predictions = model.predict(X_validate)
        print(name)
        print(accuracy_score(Y_validate, predictions))
        print(confusion_matrix(Y_validate, predictions))
        print(classification_report(Y_validate, predictions))

def predictAna(myData):
    # Drop unnecessary attributes. The elec_mwh and gas_mcf attributes should be dropped because they can generate the class labels.
    myData.drop(['state_id', 'city', 'elec_mwh', 'gas_mcf'], axis = 1, inplace = True)
    print("-----------------electricity degree prediction---------------")
    (X_train, Y_train, X_validate, Y_validate) = evaluateAlg(myData, 6)
    validateData(X_train, Y_train, X_validate, Y_validate)
    print("-----------------natural gas degree prediction---------------")
    (X_train, Y_train, X_validate, Y_validate) = evaluateAlg(myData, 7)
    validateData(X_train, Y_train, X_validate, Y_validate)

if __name__ == "__main__":
    # Get the useful attributes.
    myData = extractAttrs()
    # Calculate the mean, median and standard deviation of numeric attributes.
#    statisticalAnalysis(myData)
    binnedData = binData(myData)
    # Calculate the fraction of missing values of raw data.
    findMissing(binnedData)
    # Bin the two class attributes into 5 bins which represents 5 degrees.
    # Store the bin label into new attributes - 'elec_degree', 'gas_degree'
    binClass(binnedData)
    # Use LOF algorithm to detect outliers.
    LOF(myData)
    # Compare binning method and LOF.
    compare(myData, binnedData)
    # Plot the Histogram of the sub-dataset.
    plotData(binnedData)
    # Calculate the correlation matrix and plot the scatter plots.
    correlation(binnedData)
    # Use 3 different ways to cluster data.
    clustering(binnedData)
    # Association Rule
    associationRule(binnedData)
    # Predictive Analysis
    predictAna(binnedData)
