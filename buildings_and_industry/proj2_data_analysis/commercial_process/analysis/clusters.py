import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_samples, silhouette_score

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



if __name__ == "__main__":
    df=readData('cleaned_energy_commercial.csv')
    # df.hist()
    # fig1=plt.gcf()

    # plt.title('Histograme of Commercial Data')
    # plt.show()
    # fig1.savefig('hist.jpg')
    # plt.clf()

    df1=df.copy()
    clusterKMeans(df1)

    df2=df.copy()
    clusterWard(df2)

    