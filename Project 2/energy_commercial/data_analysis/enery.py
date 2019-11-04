import sys
import numpy as np
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn.neighbors import LocalOutlierFactor
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn import decomposition
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

def main(argv):
    print('**start**')
    ## read data ##
    pd.set_option('display.float_format',lambda x : '%.10f' % x) # cancel scientific counting
    myData = readData()

    ## basic statistical analysis ##
    calStatisic(myData)
    myData = handleOutliers(myData)
    myData = localOutlierF(myData)
    myData = binData(myData)

    ## Histograms and Correlations ##
    plotHistograms(myData)
    plotScatter(myData)

    ## Cluster Analysis ##
    numerica_myData = numericFeature(myData)
    normalize_myData = normalized(numerica_myData)
    df_cluster = normalize_myData.drop(myData.columns[[0,1,11,12]], axis=1)
    hierarchical(df_cluster)
    kMeans(df_cluster)
    DBscan(df_cluster)

    ## Association Rules ##
    associateRule(myData)

    ## Hypothesis Testing & Classification ##
    tTest(normalize_myData)
    ANOVA(normalize_myData)
    LogRegression(normalize_myData)
    predictModels(normalize_myData)

    print('**end**')

def readData():
    print('**read data start**')
    print('read data from energy_commercial.csv file and generate a dataframe named myData')
    myData = pd.read_csv('energy_commercial.csv', sep=',', encoding='latin1')
    print('**read data end**')
    print()
    return myData

def calStatisic(myData):
    print('**calculate statisic start**')
    # calculate mean, median, and std of this dataframe except for city and state
    mean = myData.iloc[:, 2:].mean()
    median = myData.iloc[:, 2:].median()
    std = myData.iloc[:, 2:].std()

    # transform the type from series to dataframe
    dict_mean = {'attribute': mean.index, 'mean': mean.values}
    df_mean = pd.DataFrame(dict_mean)
    dict_median = {'attribute': median.index, 'median': median.values}
    df_median = pd.DataFrame(dict_median)
    dict_std = {'attribute': std.index, 'std': std.values}
    df_std = pd.DataFrame(dict_std)
    
    # merge three dataframes
    statistic_DataFrame = pd.merge(df_mean, df_median)
    statistic_DataFrame = pd.merge(statistic_DataFrame, df_std)
    
    print('the statistic result is:')
    pprint(statistic_DataFrame)

    statistic_DataFrame.to_csv("statistic.csv", index = False, float_format='%.2f')
    print('**calculate statisic end**')
    print()
   
def handleOutliers(myData):
    print('**handle outliers start**')
    # load the statistics which calculate in the calStartistic() function
    df_statistic = pd.read_csv('statistic.csv', sep=',', encoding='latin1')
    # list the attributes which are needed to be processed
    attributes = ['elec_score','gas_score','num_establishments', 'elec_1kdollars', 
                  'elec_mwh', 'gas_1kdollars', 'gas_mcf', 'elec_lb_ghg','gas_lb_ghg']

    # print the original statistics
    printStatisitcs(myData, 'original')

    # use boxplot to identify outliers
    boxplot= myData.iloc[:, 2:].boxplot(return_type='dict')

    print('calculate the number of outliers in each attribute and replace them with its corresponding median:')
    for i in range(0, 9):
        outliers = boxplot['fliers'][i].get_ydata()
        outliers.tolist()
        print(attributes[i],' has ',len(outliers),' outliers')
        # obtain the corresponding median
        median = df_statistic.iloc[i,2]
        # replace the outliers with median
        myData.loc[myData[attributes[i]].isin(outliers), attributes[i]] = median
    
    # print the revised statisitcs
    printStatisitcs(myData, 'revise')

    myData.to_csv("cleaned_energy_commercial.csv", index=False)
    print('**handle outliers end**')
    print()

    return myData

def printStatisitcs(myData, name):
    statistics = myData.iloc[:, 2:].describe() # Save the basic statistics

    statistics.loc['median'] = myData.iloc[:, 2:].median() # median
    statistics.loc['range'] = statistics.loc['max']-statistics.loc['min'] # range
    statistics.loc['var'] = statistics.loc['std']/statistics.loc['mean'] # variance
    statistics.loc['dis'] = statistics.loc['75%']-statistics.loc['25%'] # interquartile range

    statistics.to_csv("statisitc_" + name + ".csv", float_format='%.2f')

def localOutlierF(myData):
    print('**local outlier factor start**')
    x = [0, 1]
    # drop the attribute city, state
    df_lof = myData.drop(myData.columns[x], axis=1)
    valueArray = df_lof.values
    X = valueArray[:, 0:9]
    
    for k in [50, 100, 200]:
        lof = LocalOutlierFactor(n_neighbors=k, contamination=0.1)   
        # return an array, -1 represents outlier while 0 represents inliers  
        y_pred = lof.fit_predict(X)
        myData['lof_outlier'] = lof.fit_predict(X) 
        # contradict with LOF score; the smaller the value, the more likely it is to be an outlier
        X_scores = lof.negative_outlier_factor_
        myData['lof_score'] = lof.negative_outlier_factor_ 
        # calculate the outliers number
        outlier_num = myData.loc[myData['lof_score'] < -2].shape[0]
        print('For k=',k, ': the outlier number is ',outlier_num)
        # when k equals 200, drop the outliers
        if k == 200:
            # sort the dataframe based on the lof score
            df_sort = myData.sort_values(by=['lof_score'], ascending = True)
            df_sort.to_csv('lof_score.csv', index=False)
            # drop the outliers and generate a new clean dataframe
            myData = myData[myData['lof_score'] > -2]
            myData = myData.copy()
            myData.drop(myData.columns[[11,12]], axis=1, inplace=True)
            myData.to_csv('lof_energy_commercial.csv', index=False)

    print('**local outlier factor end**')
    print()
    return myData

def binData(myData):
    print('**bin data start**')
    attributes = ['elec_mwh', 'gas_mcf']
    
    for attribute in attributes:
        # print(attribute)
        bins = generateBins(myData, attribute, 5)
        binName = attribute + '_bin'
        # myData[binName] = pd.cut(myData[attribute], bins)
        # Create a new variable ReactionGroups that groups posts into bins
        myData[binName] = np.digitize(myData[attribute], bins)
        # Print Bin Counts
        print("For", attribute, ', the bin result is:')
        pprint(myData[binName].value_counts())
        # generate new class
        myData.loc[myData[binName] == 1, binName] = 'Normal'
        myData.loc[(myData[binName] == 2) | (myData[binName] == 3), binName] = 'High'
        myData.loc[(myData[binName] == 4) | (myData[binName] == 5), binName] = 'Extremely High'

    myData.rename(columns={'elec_mwh_bin':'elec_class', 'gas_mcf_bin':'gas_class'}, inplace=True)
    myData.to_csv('labeled_energy_commercial.csv', index=False)

    print('**bin data end**')
    print()
    return myData

def generateBins(myData, attribute, binNum):
    # Compute min and max values, then add 1 to each side.
    minNums = myData[attribute].min()-1
    maxNums = myData[attribute].max()+1
    # print(minNums, maxNums) 

    # Create even spaced bins using min and max
    n_bin = binNum # Number of bin
    step = (maxNums - minNums) / n_bin
    bins =  np.arange(minNums, maxNums + step, step)

    return bins

def plotHistograms(myData):
    print('**plot histograms start**')
    myData.hist()
    plt.show()
    print('**plot histograms  start**')

def plotScatter(myData):
    print('**plot scatter start**')
    # drop the unrelated attributes
    scatter_myData = myData.copy()
    x = [0, 1, 2, 3, 4, 7, 8, 10, 11, 12] 
    scatter_myData.drop(scatter_myData.columns[x], axis=1, inplace=True)
    # scatter plot matrix
    scatter_matrix(scatter_myData)
    plt.show()
    print('**plot scatter start**')
    print()

def numericFeature(myData):
    print('**numeric feature start**')
    numeric_myData = myData.copy()
    attributes = ['city', 'state_abbr', 'elec_class', 'gas_class']
    for attribute in attributes:  
        numeric_myData[attribute] = pd.Categorical(numeric_myData[attribute])
        numeric_myData[attribute] = numeric_myData[attribute].cat.codes
    print('**numeric feature end**')
    return numeric_myData

def normalized(myData):
    print('**normalization start**')
    x = myData.values # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    columns = ['city', 'state_abbr', 'elec_score','gas_score','num_establishments', 'elec_1kdollars', 
               'elec_mwh', 'gas_1kdollars', 'gas_mcf', 'elec_lb_ghg','gas_lb_ghg','elec_class', 'gas_class']
    normalizedDataFrame = pd.DataFrame(data=x_scaled, columns = columns)
    print('**normalization end**')
    print()
    return normalizedDataFrame

def hierarchical(myData):
    print('**hierarchical start**')
    # Create clusters 
    k = 3
    hier = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward')
    cluster_labels = hier.fit_predict(myData)
    # Determine if the clustering is good
    silhouette_avg = metrics.silhouette_score(myData, cluster_labels)
    calinski_avg  = metrics.calinski_harabasz_score(myData,cluster_labels)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)
    print("For n_clusters =", k, "The average calinski_harabaz_score is :", calinski_avg)

    childrens = hier.children_
    # print(childrens)

    plotPCA(myData, cluster_labels, '_hierachical')

    print('**hierarchical end**')
    print()

def kMeans(myData):
    print('**k-means start**')
    # Create clusters 
    k = 3
    kmeans = KMeans(n_clusters=k)
    cluster_labels = kmeans.fit_predict(myData)
    # Determine if the clustering is good
    silhouette_avg = metrics.silhouette_score(myData, cluster_labels)
    calinski_avg  = metrics.calinski_harabasz_score(myData,cluster_labels)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)
    print("For n_clusters =", k, "The average calinski_harabaz_score is :", calinski_avg)

    centroids = kmeans.cluster_centers_
    # pprint(cluster_labels)
    # pprint(centroids)

    plotPCA(myData, cluster_labels, '_kmeans')

    print('**k-means end**')
    print()

def DBscan(myData):
    print('**dbscan start**')
    # Create clusters 
    eps = 0.1 
    samples = 50 
    cluster_labels = DBSCAN(eps=eps, min_samples=samples).fit_predict(myData)
    # Determine if the clustering is good
    silhouette_avg = metrics.silhouette_score(myData, cluster_labels)
    calinski_avg  = metrics.calinski_harabasz_score(myData,cluster_labels)
    print("For eps =", eps, "and min_samples =", samples, "The average silhouette_score is :", silhouette_avg)
    print("For eps =", eps, "and min_samples =", samples, "The average calinski_harabaz_score is :", calinski_avg)

    # pprint(cluster_labels)

    plotPCA(myData, cluster_labels, '_dbscan')

    print('**dbscan end**')
    print()

def plotPCA(myData, cluster_labels, name):
    # convert high dimensional data to 2 dimensions using PCA
    pca2D = decomposition.PCA(2)

    # Turn the NY Times data into two columns with PCA
    pca2D = pca2D.fit(myData)
    plot_columns = pca2D.transform(myData)

    # This shows how good the PCA performs on this dataset
    print(pca2D.explained_variance_)

    # Plot using a scatter plot and shade by cluster label
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels)
    plt.title("2-dimensional scatter plot using PCA" + name)

    # Write to file
    plt.savefig("pca2D" + name + ".png")

    # Clear plot
    plt.clf()

def associateRule(myData):
    print('**associate rule start**')
    # drop the unrelated attributes
    x = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    df_apriori = myData.drop(myData.columns[x], axis=1)
    # change the class name in order to distinguish the electricity class and gas class
    attributes = ['elec_class', 'gas_class']
    for attribute in attributes:
        df_apriori.loc[df_apriori[attribute] == 'Normal', attribute] = attribute + '_Normal'
        df_apriori.loc[df_apriori[attribute] == 'High', attribute] = attribute + '_High'
        df_apriori.loc[df_apriori[attribute] == 'Extremely High', attribute] = attribute + '_Extremely_High'
    print(df_apriori[0:5])
    # encode the dataframe  and train the model
    valueArray = df_apriori.values
    te = TransactionEncoder()
    te_ary = te.fit(valueArray).transform(valueArray)
    df_apriori = pd.DataFrame(te_ary, columns=te.columns_)
    # show the results for 3 different level of min_supprot
    for support in [0.1, 0.06, 0.05]:
        print('for min_support =', support)
        # generate the frequent itemsets
        frequent_itemsets = apriori(df_apriori, min_support=support, use_colnames=True)
        # frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        # frequent_itemsets = frequent_itemsets[~(frequent_itemsets['length']==1)]
        # sort the frequent items based on the support value
        frequent_itemsets = frequent_itemsets.sort_values(by=['support'], ascending = False)
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.07)
        print(frequent_itemsets)
        # print(frequent_itemsets.shape[0])
        x = [2, 3, 6, 7, 8]
        rules = rules.drop(rules.columns[x], axis=1)
        # sort the frequent items based on the support value
        rules = rules.sort_values(by=['confidence'], ascending=False)
        print(rules)

    print('**associate rule end**')
    print()

def tTest(myData):
    print('**t test start**')
    # extract attribute elec_score
    t = myData.iloc[:,2]
    # extract attribute gas_score
    a = myData.iloc[:,3]
    # judge the homogeneity of variance
    print(stats.levene(a, t)) 
    # show the results
    print(stats.ttest_ind(a,t)) 
    print('**t test end**')
    print()

def ANOVA(myData):
    print('**ANOVA start**')
    formula = 'elec_class ~ elec_1kdollars'
    anova_results = anova_lm(ols(formula,myData).fit())
    print(anova_results) 
    print('**ANOVA end**')
    print()

def LogRegression(myData):
    print('**Logistic Regression start**')
    df_logistic = myData.drop(myData.columns[[0,1,3,6,7,8,10,12]], axis=1)
    X_train, X_validate, Y_train, Y_validate = loadData(df_logistic, 4, 4)

    model = sm.Logit(Y_train, X_train)
    result = model.fit()
    print(result.summary())

    print('**Logistic Regression end**')
    print()

def predictModels(myData):
    print('**Predict model start**')
    df_model = myData.drop(myData.columns[[0,1,6,8]], axis=1)
    df_model.loc[df_model['elec_class'] == 0.5, 'elec_class'] = 2
    df_model.loc[df_model['gas_class'] == 0.5, 'gas_class'] = 2
    print('Predict electricity class:')
    models(df_model,7)

    print('Predict gas class:')
    models(df_model,8)

    print('**Predict model end**')

def models(myData,num):
    X_train, X_validate, Y_train, Y_validate = loadData(myData, 7, num)
    # Setup 10-fold cross validation to estimate the accuracy of different models
    # Split data into 10 parts
    # Test options and evaluation metric
    num_folds = 10
    seed = 7
    scoring = 'accuracy'

    # Add each algorithm and its name to the model array
    models = []
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('BAYE', GaussianNB()))
    models.append(('SVM', SVC(gamma='auto')))
    models.append(('RandomForest', RandomForestClassifier(n_estimators=10)))
    
    # Evaluate each model, add results to a results array,
    # Print the accuracy results (remember these are averages and std
    results = []
    names = []
    for name, model in models:
        print('##',name,'##')
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=False)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print('The accuracy of train set for ',msg)

        model.fit(X_train, Y_train)
        predictions = model.predict(X_validate)

        print('The accuracy of validate set is ', accuracy_score(Y_validate, predictions))
        print(confusion_matrix(Y_validate, predictions))
        print(classification_report(Y_validate, predictions))

def loadData(myData, x_num, y_num):
    valueArray = myData.values
    X = valueArray[:, 0:x_num]
    Y = valueArray[:, y_num]
    test_size = 0.20
    seed = 7
    X_train, X_validate, Y_train, Y_validate = train_test_split(X, Y, test_size=test_size, random_state=seed)

    return X_train, X_validate, Y_train, Y_validate

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)