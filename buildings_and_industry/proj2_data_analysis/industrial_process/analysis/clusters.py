# K Means
# Hierarchical - Ward
# DBScan
# Association Rules
# Histogram
# Correlation

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import decomposition
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
pd.options.display.width=0

def readData(file_name):
    df=pd.read_csv(file_name, sep=',')
    return df

def openFile(file_name):
    f=open(file_name, 'w')
    return f

def correlation(myData):
    df=pd.DataFrame()
    df['elec_mwh']=myData['elec_mwh']
    df['gas_mcf']=myData['gas_mcf']
    df['num_establishments']=myData['num_establishments']

    _corr=df.corr()
    print(_corr)
    # Plot scatter of dataframe of correlation.
    scatter_matrix(df)
    fig1=plt.gcf()
    plt.show()
    fig1.savefig('correlation.png')
    plt.clf()

def clusterKMeans(df):
    # K-Means
    df=df.drop(df.columns[[0, 1]], axis=1)

    concat_ls=[]
    key_ls=[]
    for i in df:
        concat_ls.append(df[i])
        key_ls.append(i)

    df=pd.concat(concat_ls, axis=1, keys=key_ls)
    x=df.values
    min_max_scaler=preprocessing.MinMaxScaler()
    x_scaled=min_max_scaler.fit_transform(x)
    normalizedDataFrame=pd.DataFrame(x_scaled)
    # print(normalizedDataFrame[:10])

    k=5
    kmeans=KMeans(n_clusters=k)
    cluster_labels=kmeans.fit_predict(normalizedDataFrame)

    silhouette_avg=silhouette_score(normalizedDataFrame, cluster_labels)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)

    # centroids=kmeans.cluster_centers_
    # print(cluster_labels)
    # print(centroids)

    # for i in range(len(key_ls)-1):
    #     print(pd.crosstab(cluster_labels, df[key_ls[i]]))
    plotPCA(normalizedDataFrame, 'KMeans', cluster_labels)

def clusterWard(df):
    # Hierarchical cluster - ward
    df=df.drop(df.columns[[0, 1]], axis=1)

    concat_ls=[]
    key_ls=[]
    for i in df:
        concat_ls.append(df[i])
        key_ls.append(i)

    df=pd.concat(concat_ls, axis=1, keys=key_ls)
    x=df.values
    min_max_scaler=preprocessing.MinMaxScaler()
    x_scaled=min_max_scaler.fit_transform(x)
    normalizedDataFrame=pd.DataFrame(x_scaled)
    # print(normalizedDataFrame[:10])

    k=5
    ward=AgglomerativeClustering(n_clusters=k, linkage='ward')

    cluster_labels=ward.fit_predict(normalizedDataFrame)

    silhouette_avg=silhouette_score(normalizedDataFrame, cluster_labels)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)

    # centroids=ward.cluster_centers_
    # print(cluster_labels)
    # print(centroids)

    # for i in range(len(key_ls)-1):
    #     print(pd.crosstab(cluster_labels, df[key_ls[i]]))
    plotPCA(normalizedDataFrame, 'Ward', cluster_labels)

def clusterDBScan(df):
    df=df.drop(df.columns[[0, 1]], axis=1)

    concat_ls=[]
    key_ls=[]
    for i in df:
        concat_ls.append(df[i])
        key_ls.append(i)

    df=pd.concat(concat_ls, axis=1, keys=key_ls)
    x=df.values
    min_max_scaler=preprocessing.MinMaxScaler()
    x_scaled=min_max_scaler.fit_transform(x)
    normalizedDataFrame=pd.DataFrame(x_scaled)
    # print(normalizedDataFrame[:10])

    dbs=DBSCAN(eps=0.3, min_samples=10)
    cluster_labels=dbs.fit_predict(normalizedDataFrame)

    silhouette_avg=silhouette_score(normalizedDataFrame, cluster_labels)
    print("The average silhouette_score is :", silhouette_avg)

    plotPCA(normalizedDataFrame, 'DBScan', cluster_labels)

def plotPCA(normalizedDataFrame, mode, cluster_labels):
    #####
    # PCA
    # Let's convert our high dimensional data to 2 dimensions
    # using PCA
    pca2D=decomposition.PCA(2)

    # Turn the NY Times data into two columns with PCA
    pca2D=pca2D.fit(normalizedDataFrame)
    plot_columns=pca2D.transform(normalizedDataFrame)

    # This shows how good the PCA performs on this dataset
    print(mode+' PCA 2D Explained Varience : ', pca2D.explained_variance_)

    # Plot using a scatter plot and shade by cluster label
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels)
    plt.title(mode+" : 2-dimensional scatter plot using PCA")

    # Write to file
    plt.savefig(mode+"-pca2D.png")

    # Clear plot
    plt.clf()

def associationRules(myData):
    df=pd.DataFrame()
    attrs=['elec_class', 'gas_class']
    df['elec_class']=myData['elec_bin_group']
    df['gas_class']=myData['gas_bin_group']

    # Convert group to class representation
    for attr in attrs:
        df[attr][df[attr]==1]=attr+"_normal"
        df[attr][df[attr]==2]=attr+"_high"
        df[attr][df[attr]==3]=attr+"_very_high"

    valueArray=df.values
    _encoder=TransactionEncoder()
    encoder_labels=_encoder.fit(valueArray).transform(valueArray)
    df=pd.DataFrame(encoder_labels, columns=_encoder.columns_)
    frequent_itemsets=apriori(df, min_support=0.05, use_colnames=True) 

    print(frequent_itemsets)
    result=association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)
    print(result)


if __name__=="__main__":

    print('Running clusters')
    # Read data
    df=readData('cleaned_energy_industrial.csv')

    # Histogram of Industrial Data
    # Correlation
    df.hist()
    plt.title('Histograme of Industrial Data')
    fig1=plt.gcf()
    plt.show()
    fig1.savefig('hist.jpg')
    plt.clf()

    correlation(df)

    # Clusters
    # K Means
    # Hierarchical - Ward
    # DBScan
    df1=df.copy()
    clusterKMeans(df1)

    df2=df.copy()
    clusterWard(df2)

    df3=df.copy()
    clusterDBScan(df3)

    # Assciation Rules
    associationRules(df)

    