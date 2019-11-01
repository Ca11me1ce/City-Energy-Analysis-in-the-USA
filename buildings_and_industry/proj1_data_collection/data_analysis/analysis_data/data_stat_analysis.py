import pandas as pd
pd.options.display.width = 0

def read_data(file_name):
    df=pd.read_csv(file_name, sep=',')
    return df

if __name__=='__main__':
    df=read_data('../process_data/commercial_analysis.csv')

    # Zip and naics_3 are numeric categories
    # They are meaningless in mean/median/std
    df1=df.drop(columns=['zip', 'naics_3'])

    print(df.info())

    # Get mean, median, std of continues attr
    print(df1.describe())
    df1.describe().to_csv('numerica_stat_record.csv', sep=',')

    # Get mode
    df.mode().to_csv('categorical_stat_record.csv', sep=',')
    print(df.mode())
