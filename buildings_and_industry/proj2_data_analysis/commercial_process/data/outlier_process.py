import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
pd.options.display.width=0

def localOutlierFactor(data, predict, k):
    
    # LOF
    clf=LocalOutlierFactor(n_neighbors=k+1, algorithm='auto', contamination=0.1, n_jobs=-1)
    clf.fit(data)

    # Computer k-neatest-point distance
    predict['k distances']=clf.kneighbors(predict)[0].max(axis=1)

    # Record LOF，process negative values
    predict['local outlier factor']=-clf._decision_function(predict.iloc[:, :-1])
    return predict

def plot_lof(result, method, k):
    
    # Plot LOF
    plt.rcParams['axes.unicode_minus']=False
    plt.figure(figsize=(8, 4)).add_subplot(111)
    plt.scatter(result[result['local outlier factor']>method].index,
                result[result['local outlier factor']>method]['local outlier factor'], c='blue', s=50,
                marker='.', alpha=None,
                label='Outliers')
    plt.scatter(result[result['local outlier factor']<=method].index,
                result[result['local outlier factor']<=method]['local outlier factor'], c='green', s=50,
                marker='.', alpha=None, label='Normal')
    plt.hlines(method, -2, 2+max(result.index), linestyles='--')
    plt.xlim(-2, 2+max(result.index))
    plt.title('K='+str(k)+', LOF Outlier Detector', fontsize=13)
    plt.xlabel('Index', fontsize=15)
    plt.ylabel('Outlier Factor', fontsize=15)
    plt.legend()
    fig1=plt.gcf()
    plt.show()
    fig1.savefig('outliers_'+str(k)+'.png')

def lof(data, predict=None, k=5, method=1, plot=False):
    
    # Process predict data
    predict=data.copy()

    # Compute LOF
    predict=localOutlierFactor(data, predict, k)
    if plot == True:
        plot_lof(predict, method, k)

    # Determine ouliers and inliers
    outliers=predict[predict['local outlier factor']>method].sort_values(by='local outlier factor')
    inliers=predict[predict['local outlier factor']<=method].sort_values(by='local outlier factor')
    return outliers, inliers


def readData(file_name):
    df=pd.read_csv(file_name, sep=',')
    return df

def openFile(file_name):
    f=open(file_name, 'w')
    return f

if __name__ == "__main__":
    df=readData('energy_commercial.csv')

    f=openFile('commercial_record.txt')
    # # Mean/median/std data
    # f.write('Mean/median/std\n'+str(df.describe()))

    # LOF algorithm
    # Set LOF score to 1.2
    x=[0, 1]
    df1=df.drop(df.columns[x], axis=1)

    f.write('\nLOF Algorithm:\n')
    for k in [100, 200, 500]:
        outliers, inliers=lof(data=df1, k=k, plot=True, method=1)
        print('k='+str(k)+' : '+str(len(outliers))+' outliers')
        f.write('k='+str(k)+' : '+str(len(outliers))+' outliers\n')
        outliers.to_csv('outliers_'+str(k)+'.csv', sep=',')

        if k==200:
            outlier_df=outliers

    # Choose k=500 result
    out_index=outlier_df.index.to_list()
    f.write('\nOutlier Indexes: '+str(out_index)+'\n')

    # Remove outliers by outlier indexes
    df=df.drop(out_index)
    
    df.to_csv('cleaned_energy_commercial.csv', ',', index=False)

    # Test by LOF
    # df2=df.drop(df.columns[x], axis=1)
    # outliers, inliers=lof(data=df2, k=500, plot=True, method=1)
    # print(len(outliers))

    f.close()