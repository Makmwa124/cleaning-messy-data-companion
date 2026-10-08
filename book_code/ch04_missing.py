# 04_ch04_missing: code examples from the book
# Run from the companion folder.

from pathlib import Path
Path('output').mkdir(exist_ok=True)
import pandas as pd
import numpy as np
pd.set_option('display.width', 64)
pd.set_option('display.max_columns', 10)

raw = pd.read_csv('data/raw/mallee_customers.csv',
                  encoding='cp1252', dtype=str,
                  keep_default_na=False)


suspects = ['', 'n/a', 'na', 'none', 'null', '-',
            '?', 'unknown', 'tbc', '0']
for col in raw.columns:
    hits = raw[col].str.strip().str.lower().isin(suspects)
    if hits.any():
        print(f'{col:15} {hits.sum():4}',
              sorted(raw.loc[hits, col].unique()))


cust = pd.read_csv(
    'data/raw/mallee_customers.csv',
    encoding='cp1252', dtype=str,
    na_values=['none', '-', '?', 'unknown'])
print(cust[['email', 'loyalty_points']].isna().sum())


placeholders = {'', 'n/a', 'none', '-'}
em = raw['email'].str.strip()
raw['email'] = em.mask(em.str.lower().isin(placeholders))
print(raw['email'].isna().sum())


import io
csv = 'code,country\nNA,Namibia\nNZ,New Zealand\n'
print(pd.read_csv(io.StringIO(csv)))
print(pd.read_csv(io.StringIO(csv),
                  keep_default_na=False))


left = raw['email'].dropna().str.lower()
assert not left.isin(placeholders).any()


raw['birth_missing'] = raw['birth_date'] == ''
print(raw.groupby('signup_channel')['birth_missing']
      .agg(['size', 'mean']).round(3))


mix_all = raw['signup_channel'].value_counts(
    normalize=True)
mix_kept = raw.loc[~raw['birth_missing'],
                   'signup_channel'].value_counts(
    normalize=True)
print(pd.DataFrame({'all': mix_all,
                    'with_birth_date': mix_kept}).round(3))


rep = pd.read_excel('data/raw/sales_report.xlsx',
                    header=3)
rep = rep[rep['Store'].notna()]
print(rep[['Region', 'Store']])


rep['Region'] = rep['Region'].ffill()
print(rep[['Region', 'Store']].head(6))


stores = rep[~rep['Store'].str.contains('total')]
assert stores['Region'].notna().all()
print(stores.groupby('Region')['Store'].count())

