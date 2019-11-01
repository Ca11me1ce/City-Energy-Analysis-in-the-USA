import pandas as pd

df=pd.read_csv('cleaned_energy_commercial.csv', sep=',')

ls=df['elec_score'].to_list()
ls=sorted(ls)

print(len(ls))
for i in range(0, len(ls), int(len(ls)/13)):
    print(str(ls[i]))

print(max(ls))