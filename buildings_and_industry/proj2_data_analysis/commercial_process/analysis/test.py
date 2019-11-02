import pandas as pd

df=pd.read_csv('cleaned_energy_commercial.csv', sep=',')

ls=df['gas_mcf'].to_list()
ls=sorted(ls)


print(ls[5543])
# print(len(ls))
for i in range(0, len(ls), int(len(ls)/3)):
    print(str(ls[i]))

print(max(ls))