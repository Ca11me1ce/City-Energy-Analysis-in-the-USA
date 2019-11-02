# K Means
# Hierarchical - Ward
# DBScan

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import decomposition

def readData(file_name):
    df=pd.read_csv(file_name, sep=',')
    return df

def openFile(file_name):
    f=open(file_name, 'w')
    return f

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
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    # print(normalizedDataFrame[:10])

    k = 5
    kmeans = KMeans(n_clusters=k)
    cluster_labels = kmeans.fit_predict(normalizedDataFrame)

    silhouette_avg = silhouette_score(normalizedDataFrame, cluster_labels)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)

    # centroids = kmeans.cluster_centers_
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
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    # print(normalizedDataFrame[:10])

    k=5
    ward=AgglomerativeClustering(n_clusters=k, linkage='ward')

    cluster_labels = ward.fit_predict(normalizedDataFrame)

    silhouette_avg = silhouette_score(normalizedDataFrame, cluster_labels)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)

    # centroids = ward.cluster_centers_
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
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    # print(normalizedDataFrame[:10])

    dbs=DBSCAN(eps=0.3, min_samples=10)
    cluster_labels = dbs.fit_predict(normalizedDataFrame)

    silhouette_avg = silhouette_score(normalizedDataFrame, cluster_labels)
    print("The average silhouette_score is :", silhouette_avg)

    plotPCA(normalizedDataFrame, 'DBScan', cluster_labels)

def plotPCA(normalizedDataFrame, mode, cluster_labels):
    #####
    # PCA
    # Let's convert our high dimensional data to 2 dimensions
    # using PCA
    pca2D = decomposition.PCA(2)

    # Turn the NY Times data into two columns with PCA
    pca2D = pca2D.fit(normalizedDataFrame)
    plot_columns = pca2D.transform(normalizedDataFrame)

    # This shows how good the PCA performs on this dataset
    print(mode+' PCA 2D Explained Varience : ', pca2D.explained_variance_)

    # Plot using a scatter plot and shade by cluster label
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels)
    plt.title(mode+" : 2-dimensional scatter plot using PCA")

    # Write to file
    plt.savefig(mode+"-pca2D.png")

    # Clear plot
    plt.clf()


if __name__ == "__main__":

    # Read data
    df=readData('cleaned_energy_commercial.csv')

    # #--------------------------------------------------
    # # Histogram of Commercial Data
    # df.hist()
    # fig1=plt.gcf()

    # plt.title('Histograme of Commercial Data')
    # plt.show()
    # fig1.savefig('hist.jpg')
    # plt.clf()

    # # Clusters
    # # K Means
    # # Hierarchical - Ward
    # # DBScan
    # df1=df.copy()
    # clusterKMeans(df1)

    # df2=df.copy()
    # clusterWard(df2)

    # df3=df.copy()
    # clusterDBScan(df3)
    # #-------------------------------------------------

    # Assciation rules

    