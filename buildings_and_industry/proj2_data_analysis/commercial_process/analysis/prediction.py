import pandas as pd

def readData(file_name):
    df=pd.read_csv(file_name, sep=',')
    return df

def openFile(file_name):
    f=open(file_name, 'w')
    return f

if __name__ == "__main__":

    # Read data
    df=readData('cleaned_energy_commercial.csv')