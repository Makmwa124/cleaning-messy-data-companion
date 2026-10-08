# 01_ch01_workflow: code examples from the book
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
print(raw.shape)


def profile(df):
    return pd.DataFrame({
        'filled': (df != '').sum(),
        'blank': (df == '').sum(),
        'unique': df.nunique(),
    })

print(profile(raw))


print(raw['state'].value_counts())


print('Exact duplicate rows:', raw.duplicated().sum())
print('Repeated cust_no:', raw['cust_no'].duplicated().sum())
print(raw.sample(1, random_state=1).T)


before = len(raw)
clean = raw.drop_duplicates()
print(f'{before} rows -> {len(clean)} rows '
      f'({before - len(clean)} removed)')


assert clean.duplicated().sum() == 0
assert set(clean.columns) == set(raw.columns)

