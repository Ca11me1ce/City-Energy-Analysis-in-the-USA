import pandas as pd

df=pd.read_csv('../data/energy_industrial.csv', sep=',')
ls=df['gas_mcf'].to_list()
max_v=max(ls)
print(max_v)
_len=len(ls)
ls=sorted(ls)

for i in range(0, _len, int(_len/3)):
    print(ls[i])