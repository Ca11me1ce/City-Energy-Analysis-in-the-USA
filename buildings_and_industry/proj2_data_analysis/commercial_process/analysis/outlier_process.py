# Mean/median/std
# LOF
# Binning

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
import numpy as np
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

def plotLOF(result, method, k):
    
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
        plotLOF(predict, method, k)

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

def equalWidthBinning(myData, attr, f):
    # Compute min and max values, then add 1 to each side.
    minReactionNums = myData[attr].min() - 1
    maxReactionNums = myData[attr].max() + 1

    # Create even spaced bins using min and max
    n_bin = 10 # Number of bin
    step = (maxReactionNums - minReactionNums) / n_bin
    bins =  np.arange(minReactionNums, maxReactionNums + step, step)

    # Look at new bins. This is equi-width binning
    reactionBins = np.digitize(myData[attr], bins)

    # Count the number of values in each bin
    reactionBinCounts = np.bincount(reactionBins)
    print("\n\nBins are: \n ", reactionBins)
    f.write("\n\nBins are: \n "+str(reactionBins)+'\n')
    print("\nBin count is ", reactionBinCounts)
    f.write("\nBin count is : "+str(reactionBinCounts)+'\n')

    # Create a new variable ReactionGroups that groups posts into bins, e.g. < 200, 200-400, etc.
    # For this example, I use the bins created above
    myData['bin_group'] = np.digitize(myData[attr], bins)
    print("\nAfter bin_group is added we have:\n", myData[:10])
    f.write("\nAfter bin_group is added we have:\n"+str(myData[:10])+'\n')

    # Another option to see actual bins
    myData['bin_ranges'] = pd.cut(myData[attr], bins)

    # Print Bin Counts in different ways
    print("\nBin Counts\n")
    f.write("\nBin Counts\n")
    print(myData['bin_ranges'].value_counts())
    f.write(str(myData['bin_ranges'].value_counts())+'\n')


def equalDepthBinning(myData, attr, f):
    names = range(1,14)
    bins1=[0, 226, 505, 949, 1669, 2863, 4700, 8158, 14242, 23339, 41816, 90210, 252063, 11000000]
    # myData['bin_group'] = np.digitize(myData[attr], bins1)
    myData['bin_group'] = pd.cut(myData[attr], bins1, labels=names)

    #Check the data to see the new column
    print("\n New column of data:")
    f.write("\n New column of data: \n")
    print(myData[:10])
    f.write(str(myData[:10])+'\n')

    # Print Bin Counts in different ways
    print("\nBin Counts\n")
    f.write("\nBin Counts\n")
    print(myData['bin_group'].value_counts())
    f.write(str(myData['bin_group'].value_counts())+'\n')
    return myData


if __name__ == "__main__":
    df=readData('../data/energy_commercial.csv')

    f=openFile('commercial_record.txt')
    # Mean/median/std data
    f.write('Mean/median/std before LOF\n'+str(df.describe()))

    # LOF algorithm
    # Set LOF score to 1
    x=[0, 1]
    df1=df.drop(df.columns[x], axis=1)

    f.write('\n\nLOF Algorithm:\n')
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
    
    # Mean/median/std data
    f.write('\nMean/median/std after LOF\n'+str(df.describe()))

    # Test by LOF
    # df2=df.drop(df.columns[x], axis=1)
    # outliers, inliers=lof(data=df2, k=500, plot=True, method=1)
    # print(len(outliers))

    # Equal-width binning
    binning_attr=['elec_score', 'gas_score']
    f.write('\n\n\nEqual-width binning: \n')
    for i in binning_attr:
        df1=df.copy()
        f.write('\nattr: '+i+'\n')
        equalWidthBinning(df1, i, f)

    # Equal-depth binning
    df2=df.copy()
    f.write('\nEqual-depth binning: \n')
    f.write('\nattr: elec_score\n')
    df=equalDepthBinning(df2, 'elec_score', f)

    df.to_csv('cleaned_energy_commercial.csv', ',', index=False)

    f.close()