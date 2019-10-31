import pandas as pd

def readData(file_name):
    df=pd.read_csv(file_name, sep=',')
    return df

def openFile(file_name):
    f=open(file_name, 'a')
    return f

if __name__ == "__main__":
    df=readData('../data/energy_commercial.csv')
    print(df.info())

    f=openFile('record.txt')

    f.close()