import pandas as pd

dfs = []
for year in range(2010, 2018):
    fn = 'data/horoscope_{}.csv'.format(year)
    dfs.append(pd.read_csv(fn))
df_all_years = pd.concat(dfs)
df_all_years.to_csv('data/horoscope_dataset.csv', index = False)
